# with porcentagem_de_cashback_mes as (
# 	with cashback_acumulado_mes as (
# 		select
# 			r.id revendedor_id,
# 			date_trunc('month', c."data") mes,
# 			sum(valor) valor_acumulado
# 		from compras c
# 		inner join revendedores r
# 		on c.revendedor_id = r.id
# 		group by date_trunc('month', c."data"), r.id
# 	)
# 	select ca.*, porcentagem_de_cashback
# 	from cashback_criterios cc
# 	inner join cashback_acumulado_mes ca
# 	on cc.intervalo @> ca.valor_acumulado
# )
# select
# 	c2.*,
# 	pcm.porcentagem_de_cashback porcentagem_de_cashback,
# 	c2.valor * porcentagem_de_cashback valor_de_cashback
# from compras c2
# inner join porcentagem_de_cashback_mes pcm
# on date_trunc('month', c2."data") = pcm.mes
# where pcm.revendedor_id = '0c90e538-fb0d-4f99-80f5-334457485ea7';

from pprint import pprint
from unittest import result

from sqlalchemy import func

from app.controllers.dependencies import get_db
from app.models.cashback import CashbackCriterio
from app.models.compra import Compra
from app.models.revendedor import Revendedor

db = next(get_db())

cashback_acumulado_mes = (
    db.query(
        Revendedor.id.label("revendedor_id"),
        func.date_trunc("month", Compra.data).label("mes"),
        func.sum(Compra.valor).label("valor_acumulado"),
    )
    .join(Compra)
    .group_by(func.date_trunc("month", Compra.data), Revendedor.id)
    .cte()
)

porcentagem_de_cashback_mes = (
    db.query(
        cashback_acumulado_mes,
        CashbackCriterio.porcentagem_de_cashback.label("porcentagem_de_cashback"),
    )
    .select_from(CashbackCriterio)
    .join(
        cashback_acumulado_mes,
        CashbackCriterio.intervalo.contains(cashback_acumulado_mes.c.valor_acumulado),
    )
    .cte()
)

result = (
    db.query(
        Compra,
        porcentagem_de_cashback_mes.c.porcentagem_de_cashback.label(
            "porcentagem_de_cashback"
        ),
        (Compra.valor * porcentagem_de_cashback_mes.c.porcentagem_de_cashback).label(
            "valor_de_cashback"
        ),
    )
    .select_from(Compra)
    .join(
        porcentagem_de_cashback_mes,
        func.date_trunc("month", Compra.data) == porcentagem_de_cashback_mes.c.mes,
    )
    .filter(Compra.revendedor_id == "0c90e538-fb0d-4f99-80f5-334457485ea7")
    .order_by(Compra.data.desc())
    .all()
)


pprint(result)
