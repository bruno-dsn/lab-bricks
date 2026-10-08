"""Caderno pessoal com importação limitada; não é certificação nem autenticação."""
import json
import re


def _json(payload):
    if not isinstance(payload, bytes) or len(payload) > 100_000:
        raise ValueError('Use um JSON de até 100 KB.')
    try:
        return json.loads(payload)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise ValueError('JSON inválido.') from None


def validar_feedback(value, exercicios):
    fields = {'format','version','exercicio','passed','failed','errors','validado','codigo_sha256'}
    if not isinstance(value, dict) or set(value) != fields or value['format'] != 'lab-bricks-feedback' or type(value['version']) is not int or value['version'] != 1 or not isinstance(value['exercicio'], str) or value['exercicio'] not in exercicios:
        raise ValueError('Formato de feedback incompatível.')
    if any(type(value[k]) is not int or not 0 <= value[k] <= 1000 for k in ('passed','failed','errors')):
        raise ValueError('Contagens de feedback inválidas.')
    expected = value['passed'] > 0 and value['failed'] == value['errors'] == 0
    if type(value['validado']) is not bool or value['validado'] != expected or not isinstance(value['codigo_sha256'], str) or not re.fullmatch('[a-f0-9]{64}', value['codigo_sha256']):
        raise ValueError('Resultado ou hash de feedback inválido.')
    return value


def importar_feedback(payload, exercicios):
    return validar_feedback(_json(payload), exercicios)


def importar_caderno(payload, aulas, exercicios):
    value = _json(payload)
    if not isinstance(value, dict) or set(value) != {'format','version','reflexoes','exercicios'} or value['format'] != 'lab-bricks-caderno' or type(value['version']) is not int or value['version'] != 1:
        raise ValueError('Formato de caderno incompatível.')
    reflections = value['reflexoes']
    if not isinstance(reflections, dict) or set(reflections) - set(aulas):
        raise ValueError('Reflexão de aula desconhecida.')
    for note in reflections.values():
        if not isinstance(note, dict) or set(note) != {'texto','confianca'} or not isinstance(note['texto'], str) or len(note['texto']) > 2000 or type(note['confianca']) is not int or not 0 <= note['confianca'] <= 3:
            raise ValueError('Reflexão fora do contrato.')
    if not isinstance(value['exercicios'], dict) or set(value['exercicios']) - set(exercicios):
        raise ValueError('Exercício desconhecido.')
    for key, feedback in value['exercicios'].items():
        validar_feedback(feedback, exercicios)
        if feedback['exercicio'] != key:
            raise ValueError('ID do feedback diverge do exercício.')
    return value


def exportar_caderno(value, aulas, exercicios):
    payload = json.dumps(value, ensure_ascii=False, indent=2).encode()
    importar_caderno(payload, aulas, exercicios)
    return payload
