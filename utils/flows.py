from viewflow import fsm
from models.models.posts.models import State
from api.services.notifications.notify import NotifyService


class Flow:
    state = fsm.State(State, default=State.PEN)

    def __init__(self, obj):
        self.object = obj

    @state.setter()
    def _set_object_state(self, value):
        self.object.state = value

    @state.getter()
    def _get_object_state(self):
        return self.object.state

    @state.transition(source=[State.PEN, State.APP, State.REJ, State.DEL], target=State.PEN)
    def pending(self):
        NotifyService.send(
            user_id=self.object.author.id,
            message={'text': f'Ваш пост "{self.object.title}" на модерации.'}
        )
        return 'Статус изменен на "На модерации".'

    @state.transition(source=[State.PEN, State.APP, State.REJ, State.DEL], target=State.APP)
    def approve(self):
        NotifyService.send(
            user_id=self.object.author.id,
            message={'text': f'Ваш пост "{self.object.title}" одобрен!'}
        )
        return 'Статус изменен на "Одобрен".'


    @state.transition(source=State.PEN, target=State.REJ)
    def reject(self):
        NotifyService.send(
            user_id=self.object.author.id,
            message={'text': f'Ваш пост "{self.object.title}" отклонен.'}
        )
        return 'Статус изменен на "Отклонен".'

    @state.transition(source=[State.PEN, State.APP, State.REJ, State.DEL], target=State.DEL)
    def delete(self):
        NotifyService.send(
            user_id=self.object.author.id,
            message={'text': f'Ваш пост "{self.object.title}" будет удален через 10 секунд.'}
        )
        return 'Статус изменен на "На удалении".'
