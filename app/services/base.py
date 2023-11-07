from sqlalchemy.orm import Session


class BaseDataManager:
    def __init__(self, session: Session):
        self.session = session

    def add_one(self, model):
        self.session.add(model)
        self.session.commit()

    def get_one(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs).first()

    def get_all(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs).all()

    def update(self, model, updated_data: dict):
        for key, value in updated_data.items():
            setattr(model, key, value)
        self.session.commit()

    def delete(self, model):
        self.session.delete(instance=model)
        self.session.commit()


class BaseService:
    def __init__(self, session, manager):
        self.session = session
        self.manager = manager

    def create(self, data):
        return self.manager.add_one(data)

    def get(self, model, **kwargs):
        return self.manager.get_one(model, **kwargs)

    def update(self, model, filters, update_data):
        return self.manager.update(model, filters, update_data)

    def delete(self, model):
        return self.manager.delete(model)
