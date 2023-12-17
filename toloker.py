from config import config
import toloka.client as toloka
from settings import admins

# Инициализация Толоки
TOLOKA = config.TOLOKA
toloka_client = toloka.TolokaClient(TOLOKA, 'PRODUCTION')
POOL = '42510184'


def toloker_accept(ass_id: str) -> bool:
    try:
        toloka_client.accept_assignment(assignment_id=ass_id, public_comment='Thank you')
        return True
    except Exception as e:
        print('accept error', ass_id)
        print(e)
        return False


def toloker_reject(ass_id: str, reason: str) -> bool:
    try:
        toloka_client.reject_assignment(assignment_id=ass_id, public_comment=reason)
        return True
    except Exception as e:
        print('reject error', ass_id)
        print(e)
        return False


def tlk_ass_by_tg_id(telegram_id: str) -> str:
    if telegram_id in admins:
        return
    assignments = toloka_client.get_assignments(pool_id=POOL, batch_size=1000)
    # перебор всех сабмитов
    print('поиск толокера, tg id', telegram_id)
    for ass in assignments:
        status = ass.status.value
        if status in 'SUBMITTED':
            # смотрим, что толокер указал в качестве Telegram-id
            output_tg_id = ass.solutions[0].output_values.get('tg_id')
            if telegram_id in output_tg_id:
                print('найден')
                return ass.id
    print('не найден')


