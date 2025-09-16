from agents import Agent, Runner, SQLiteSession, function_tool
from pathlib import Path
import argparse


def _read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Arquivo de prompt não encontrado: {path}")
    return p.read_text(encoding="utf-8")


@function_tool
def obter_dump() -> str:
    """
    Tool A — Coletar notícias recentes (IA/Tech), pesquisas, lançamentos e regulações.
    Deve retornar um dump organizado (JSON ou Markdown) com título, resumo curto, data e link.
    """
    ...


@function_tool
def validar_e_formatar(dump: str) -> str:
    """
    Tool B — Validar e enriquecer o dump com análise econômica, impactos e por que importa.
    Retorna os itens revisados com metadados completos prontos para o documento final.
    """
    ...


def main() -> int:
    parser = argparse.ArgumentParser(description="Resumo semanal IA/Tech com agentes e orquestração")
    parser.add_argument(
        "--db-path",
        default=str(Path("db") / "digest_weekly.sqlite"),
        help="Caminho do arquivo SQLite local (ex.: db/digest_weekly.sqlite)",
    )
    args = parser.parse_args()

    # Carrega instruções e prompt do usuário a partir de arquivos editáveis por não-TI
    reporter_instr = _read_text("prompts/reporter.md")
    economista_instr = _read_text("prompts/economista.md")
    orquestrador_instr = _read_text("prompts/orquestrador.md")
    user_prompt = _read_text("prompts/usuario_base.md")

    reporter = Agent(
        name="Repórter",
        instructions=reporter_instr,
        tools=[obter_dump],
    )

    economista = Agent(
        name="Economista",
        instructions=economista_instr,
        tools=[validar_e_formatar],
    )

    orquestrador = Agent(
        name="Orquestrador",
        instructions=orquestrador_instr,
        handoffs=[reporter, economista],
    )

    # Garante que o banco fique em um caminho local controlado
    db_path = Path(args.db_path)
    if db_path.parent and not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
    session = SQLiteSession(str(db_path))

    result = Runner.run_sync(orquestrador, user_prompt, session=session)
    print(result.final_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
