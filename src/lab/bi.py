"""Um segundo caso: pedidos com vários itens e dimensões sintéticas."""
from datetime import date, timedelta
import random
import pandas as pd


def gerar_comercio(n=180, seed=42):
    if type(n) is not int or not 30 <= n <= 500 or type(seed) is not int or not 0 <= seed <= 1000:
        raise ValueError("Use de 30 a 500 pedidos e semente entre 0 e 1000.")
    rng = random.Random(seed)
    clientes = [{"cliente_id": i, "segmento": ["pessoa", "empresa"][i % 2], "regiao": ["Norte", "Sul", "Sudeste"][i % 3]} for i in range(1, 31)]
    produtos = [{"produto_id": i, "produto": name, "categoria": cat, "preco_centavos": price, "custo_centavos": cost} for i, (name, cat, price, cost) in enumerate([
        ("Caderno", "Papelaria", 2400, 1300), ("Caneta", "Papelaria", 800, 300), ("Mochila", "Acessórios", 12000, 7500), ("Garrafa", "Acessórios", 4500, 2100), ("Livro", "Leitura", 6500, 3900), ("Marcador", "Leitura", 900, 250)], 1)]
    pedidos, itens = [], []
    for i in range(1, n + 1):
        pedidos.append({"pedido_id": i, "cliente_id": rng.randrange(1, 31), "data_pedido": (date(2026, 1, 1) + timedelta(days=(i - 1) * 90 // n)).isoformat(), "canal": rng.choice(["site", "loja", "app"]), "status": "cancelado" if i % 11 == 0 else "concluido"})
        for product in rng.sample(produtos, rng.randrange(1, 4)):
            itens.append({"item_id": len(itens) + 1, "pedido_id": i, "produto_id": product["produto_id"], "quantidade": rng.randrange(1, 5), "preco_unitario_centavos": product["preco_centavos"], "custo_unitario_centavos": product["custo_centavos"]})
    return {"clientes": pd.DataFrame(clientes), "produtos": pd.DataFrame(produtos), "pedidos": pd.DataFrame(pedidos), "itens_pedido": pd.DataFrame(itens)}


def fatos(tabelas):
    rows = tabelas["itens_pedido"].merge(tabelas["pedidos"], on="pedido_id", validate="many_to_one").merge(tabelas["clientes"], on="cliente_id", validate="many_to_one").merge(tabelas["produtos"][["produto_id", "produto", "categoria"]], on="produto_id", validate="many_to_one")
    rows["receita_centavos"] = rows["quantidade"] * rows["preco_unitario_centavos"]
    rows["custo_centavos"] = rows["quantidade"] * rows["custo_unitario_centavos"]
    rows["margem_centavos"] = rows["receita_centavos"] - rows["custo_centavos"]
    return rows


def resumo(tabelas):
    frame = fatos(tabelas)
    frame = frame.loc[frame["status"] == "concluido"]
    revenue = int(frame["receita_centavos"].sum())
    margin = int(frame["margem_centavos"].sum())
    return {"pedidos": int(frame["pedido_id"].nunique()), "linhas": len(frame), "unidades": int(frame["quantidade"].sum()), "receita_centavos": revenue, "margem_centavos": margin, "margem_percentual": margin / revenue * 100 if revenue else 0}


CONSULTAS = {
    "Grão: linhas versus pedidos": "SELECT COUNT(*) AS linhas, COUNT(DISTINCT p.pedido_id) AS pedidos\nFROM pedidos p JOIN itens_pedido i ON p.pedido_id = i.pedido_id\nWHERE p.status = 'concluido';",
    "Receita e margem por categoria": "SELECT d.categoria, ROUND(SUM(i.quantidade * i.preco_unitario_centavos) / 100.0, 2) AS receita,\nROUND(SUM(i.quantidade * (i.preco_unitario_centavos-i.custo_unitario_centavos)) / 100.0, 2) AS margem_bruta\nFROM itens_pedido i JOIN pedidos p ON p.pedido_id=i.pedido_id\nJOIN produtos d ON d.produto_id=i.produto_id\nWHERE p.status='concluido' GROUP BY d.categoria ORDER BY receita DESC;",
    "Receita acumulada com janela": "WITH diario AS (\n SELECT p.data_pedido, SUM(i.quantidade*i.preco_unitario_centavos)/100.0 AS receita\n FROM pedidos p JOIN itens_pedido i ON p.pedido_id=i.pedido_id\n WHERE p.status='concluido' GROUP BY p.data_pedido\n)\nSELECT data_pedido, receita, SUM(receita) OVER (ORDER BY data_pedido ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulada\nFROM diario ORDER BY data_pedido;",
}
