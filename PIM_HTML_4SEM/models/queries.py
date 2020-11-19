from typing import Generator
from datetime import timedelta

from models import DBSession
from models.entities import Customers, cur_datetime
from sqlalchemy import asc

attempts_limit = 5


class DataHandlers(object):
    @classmethod
    def api_error_status_to_waiting_normalization(cls) -> None:
        # 1
        result = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.api_error.value,
                    Customers.current_step == Customers.CurrentStepEnum.n4_waiting_deactivation_line.value)
            .update({
                Customers.status: Customers.StatusEnum.waiting_deactivation.value,
                Customers.obs: 'Re-tentativa de api_error'
            }, synchronize_session=False)
        )

        if result:
            DBSession.commit()

    @classmethod
    def single_error_to_pending(cls) -> None:
        # 2
        result = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.single_error.value)
            .update({
                Customers.status: Customers.StatusEnum.pending.value,
                Customers.obs: 'Re-tentativa de erro do Single'
            }, synchronize_session=False)
        )

        if result:
            DBSession.commit()

    @classmethod
    def api_error_status_normalization(cls) -> None:
        # 3
        result = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.api_error.value)
            .update({
                Customers.status: Customers.StatusEnum.pending.value,
                Customers.obs: 'Re-tentativa de api_error'
            }, synchronize_session=False)
        )

        if result:
            DBSession.commit()

    @classmethod
    def robot_error_status_normalization(cls) -> None:
        # 4
        result = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.robot_error.value,
                    Customers.attempts < 5)
            .update({
                Customers.status: Customers.StatusEnum.pending.value,
                Customers.obs: 'Re-tentativa de robot_error'
            }, synchronize_session=False)
        )

        if result:
            DBSession.commit()

    @classmethod
    def attempts_validation(cls) -> None:
        # 5
        result = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.robot_error.value,
                    Customers.attempts >= 5)
            .update({
                Customers.status: Customers.StatusEnum.data_error.value,
                Customers.obs: f'Atingido o limit de {attempts_limit} tentativas'
            }, synchronize_session=False)
        )

        if result:
            DBSession.commit()

    @classmethod
    def ti_failed_validation(cls) -> None:
        # 6
        results = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.waiting_deactivation.value)
            .yield_per(100)
        )

        customers = (customer for customer in results if customer.single_conclusion_date
                     and
                     (cur_datetime().date() - customer.single_conclusion_date.date()).days > 3)

        for customer in customers:
            Customers.update_customer(id_=customer.id,
                                      current_step=Customers.CurrentStepEnum.n4_line_suspected.value,
                                      status=Customers.StatusEnum.ti_failed.value,
                                      obs='Solicitação finalizada no Single a mais de 3 dias')

    @classmethod
    def get_waiting_deactivation(cls) -> Generator:
        # 7
        results = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.waiting_deactivation.value,
                    Customers.current_step == Customers.CurrentStepEnum.n4_waiting_deactivation_line.value)
            .yield_per(100)
        )

        return (customer for customer in results if not customer.date_check_status
                or (customer.date_check_status + timedelta(hours=6)) <= cur_datetime().replace(tzinfo=None))

    @classmethod
    def get_customers_in_waiting_ra(cls) -> list:
        # 8
        results = (
            DBSession
            .query(Customers)
            .filter_by(status=Customers.StatusEnum.waiting_ra.value)
            .order_by(asc(Customers.created))
            .yield_per(100)
        )

        return [customer for customer in results if (cur_datetime() - customer.created).seconds <= 43200]

    @classmethod
    def validate_due_waiting_ra(cls) -> None:
        results = (
            DBSession
            .query(Customers)
            .filter(Customers.status == Customers.StatusEnum.waiting_ra.value)
            .yield_per(100)
        )

        for customer in results:
            if (cur_datetime().replace(tzinfo=None) - customer.created).seconds > 43200:
                Customers.update_customer(id_=customer.id,
                                          status=Customers.StatusEnum.ra_fail.value,
                                          obs='Registro criado a mais de 12 horas e pendente de localização de RA')

    @classmethod
    def ra_waiting_normalization(cls) -> None:
        results = (
            DBSession
            .query(Customers)
            .filter_by(status=Customers.StatusEnum.api_error.value,
                       current_step=Customers.CurrentStepEnum.n1_creating_register_attendance.value)
            .update({
                Customers.status: Customers.StatusEnum.waiting_ra.value,
                Customers.obs: 'Re-tentando localizar RA'
            }, synchronize_session=False)
        )

        if results:
            DBSession.commit()
