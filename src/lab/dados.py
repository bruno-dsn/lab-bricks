"""Uma fonte pequena, determinística e inteiramente fictícia."""
from datetime import date, timedelta
from random import Random


COLUNAS = [
    "venda_id", "data_venda", "produto", "categoria", "canal",
    "quantidade", "preco_unitario", "status", "atualizado_em",
]


def gerar_vendas(n=720, sujeira=True, seed=42):
    """Gera strings como um CSV recebido de outra ferramenta.

    Cada linha representa um pedido com um único produto. As seis linhas
    inválidas e uma versão repetida são adicionadas ao tamanho solicitado.
    """
    if type(n) is not int or not 90 <= n <= 2000:
        raise ValueError("Use entre 90 e 2000 pedidos.")
    if type(seed) is not int or not 0 <= seed <= 1000:
        raise ValueError("Use uma semente inteira entre 0 e 1000.")
    if type(sujeira) is not bool:
        raise ValueError("A opção de qualidade deve ser booleana.")
    rng = Random(seed)
    produtos = [
        ("Caderno", "Papelaria", "24.90"),
        ("Luminaria", "Casa", "89.90"),
        ("Fone", "Tecnologia", "159.90"),
        ("Garrafa", "Casa", "49.90"),
    ]
    rows = []
    for i in range(n):
        dia = date(2026, 1, 1) + timedelta(days=i % 90)
        produto, categoria, preco = rng.choice(produtos)
        rows.append(dict(zip(COLUNAS, [
            f"V{i+1:06d}", dia.isoformat(), produto, categoria,
            rng.choice(["Site", "Aplicativo", "Marketplace"]),
            str(rng.randint(1, 5)), preco,
            "cancelada" if rng.random() < 0.12 else "concluida",
            f"{dia.isoformat()} 10:00:00",
        ])))
    if sujeira:
        rows.append({**rows[0], "quantidade": "4", "atualizado_em": "2026-04-01 12:00:00"})
        falhas = [
            {"data_venda": "2026-02-30"}, {"quantidade": "0"},
            {"preco_unitario": "-9.90"}, {"produto": ""},
            {"status": "desconhecida"}, {"venda_id": ""},
        ]
        for i, falha in enumerate(falhas):
            rows.append({**rows[1], "venda_id": f"X{i+1:06d}", **falha})
    return rows
