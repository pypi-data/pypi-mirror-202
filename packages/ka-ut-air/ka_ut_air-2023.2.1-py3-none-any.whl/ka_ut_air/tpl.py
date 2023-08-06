"""
Source Templates
"""

# from ka_com.log import Log


class TplTsk:
    """
    Operator class
    """
    TriggerDagRun = """
{{_tsk}} = TriggerDagRunOperator(
    task_id="{{task_id}}",
    trigger_dag_id="{{trigger_dag_id}}",
    execution_date="{{execution_date}}",
    reset_dag_run=True,
    wait_for_completion=True,
    poke_interval=30,
    allowed_states=['success'],
    failed_states=None,
    params={
        "triggered_by_dag_id": "{{triggered_by_dag_id}}"
    },
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}"
)

"""

    ExternalTaskSensor = """
{{_tsk}} = ExternalTaskSensor(
    task_id="{{tsk_id}}",
    task_group={{_tg}},
    external_dag_id="{{external_dag_id}}",
    timeout=600,
    allowed_states=['success'],
    failed_states=['failed', 'skipped'],
    mode="reschedule",
)

"""

    Bash = """
{{_tsk}} = BashOperator(
    bash_command='{{command}}',
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id='{{task_id}}',
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}"
)

"""


class TplDbTsk:
    """
    Operator class
    """
    DbTriggerDagRun = """
{{_tsk}} = TriggerDagRunOperator(
    task_id="{{task_id}}",
    trigger_dag_id="{{trigger_dag_id}}",
    execution_date="{{execution_date}}",
    reset_dag_run=True,
    wait_for_completion=True,
    poke_interval=30,
    allowed_states=['success'],
    failed_states=None,
    params={
        "triggered_by_dag_id": "{{triggered_by_dag_id}}"
    },
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbApcShell = """
{{_tsk}} = DbApcShellOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbShell = """
{{_tsk}} = DbShellOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbShellCyclic = """
{{_tsk}} = DbShellCyclicOperator(
    shell="{{shell}}",
    command="{{command}}",
    parameter={{parameter|tojson}},
    sequence={{sequence}},
    interval={{interval}},
    options="{{options}}",
    appl="{{appl}}",
    run_as_user="{{run_as_user}}",
    skip_exit_code={{skip_exit_code}},
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}},
    trigger_rule="{{trigger_rule}}",
    var_tsk="{{var_tsk}}"
)

"""

    DbCond = """
{{_tsk}} = DbCondOperator(
    cond_key="{{cond_key}}",
    run_as_user="{{run_as_user}}",
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}}
)

"""

    DbFileSensorAsync = """
{{_tsk}} = DbFileSensorAsyncOperator(
    cond_key="{{cond_key}}",
    run_as_user="{{run_as_user}}",
    task_id="{{task_id}}",
    dag=dag,
    task_group={{_tg}}
)

"""


class TplTskArrDownstream:
    """
    Task Array class
    """
    s_downstream = """
{{source}}.set_downstream({{target}})"""


class TplTskGrp:

    s_child = """
{{group_id}} = TaskGroup(
     group_id='{{group_id}}',
     tooltip='{{tooltip}}',
     parent_group={{parent_group}},
     dag=dag
)

"""

    s_root = """
{{group_id}} = TaskGroup(
    group_id='{{group_id}}',
    tooltip='{{tooltip}}',
    dag=dag
)

"""


class TplDags:

    s_dag = """
import pendulum

from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.models.dag import DAG
from airflow.models.baseoperator import chain

from ka_air_prv.prv.core.operators.DbApcShell import DbApcShellOperator
from ka_air_prv.prv.core.operators.DbShell import DbShellOperator
from ka_air_prv.prv.core.operators.DbShellCyclic import DbShellCyclicOperator
from ka_air_prv.prv.core.operators.DbCond import DbCondOperator
from ka_air_prv.prv.core.operators.DbFileSensorAsnyc
    import DbFileSensorAsnycOperator
from ka_air_prv.prv.core.operators.DbTriggerDagRun
    import DbTriggerDagRunOperator

from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.bash import BashOperator

# schedule=None
# schedule_interval=timedelta(days=1)
schedule_interval=None
# start_date = days_ago(2)
start_date = pendulum.datetime(2022, 1, 1, tz="UTC")
catchup = False
skip_exit_code = None

email = ['bernd.stroehle@db.com']
email_on_failure = False

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    'email': email,
    'email_on_failure': email_on_failure,
}

dag = DAG(
    dag_id='{{dag_id}}',
    description='{{description}}',
    default_args=default_args,
    schedule_interval=schedule_interval,
    start_date=start_date,
    catchup=catchup,
    tags={{tags}},
)

"""
