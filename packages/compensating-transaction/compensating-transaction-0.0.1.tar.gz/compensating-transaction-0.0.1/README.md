# compensating-transaction

When the function execution fails, the function execution can be rolled back, and all previous function executions can be rolled back
```
For Example:
    1. step1 -> step2 -> step3
        1). if step2 execution error:
            rollback step1
        2). if step3 execution error:
            rollback step2 -> rollback step1
    2. step1 -> step2 -> step3_1, step3_2, step3_3 -> step4
        1). if step3_2 execution error:
            rollback step3_1 -> rollback step2 -> rollback step1
        2). if step4 execution error:
            rollback step3_3 -> rollback step3_2 -> rollback step3_1 -> rollback step2 -> rollback step1
    
```
# Use Example:
```
from compensating_transaction.transaction import CompensatingTransaction


def test_rollback():
    l = []
    def add_item(name):
        if name == 'l7':
            raise ValueError('not l7')
        l.append(name)

    def sub_item(name):
        if name in l:
            l.remove(name)
        print(f'run sub_item: {name}')
        return f'sub_item: {name}'

    step1 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l1',),
        rollback_func=sub_item,
        rollback_args=('l1',),
    )
    step1.run()
    step2 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l2',),
        rollback_func=sub_item,
        rollback_args=('l2',),
        previous=step1,
    )
    step2.run()
    step3 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l3',),
        rollback_func=sub_item,
        rollback_args=('l3',),
        previous=step2,
        rollback_exe=AttributeError,
    )
    step3.run()
    step4 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l4',),
        rollback_func=sub_item,
        rollback_args=('l4',),
        previous=step3,
        rollback_exe=AttributeError,
    )
    step4.run()
    step4_1 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l4-1',),
        rollback_func=sub_item,
        rollback_args=('l4-1',),
        previous=step3,
        rollback_exe=AttributeError,
    )
    step4_1.run()
    step5 = CompensatingTransaction(
        run_func=add_item,
        run_args=('l5',),
        rollback_func=sub_item,
        rollback_args=('l5',),
        previous=[step4, step4_1],
        rollback_exe=AttributeError,
    )
    step5.run()
    assert l == ['l1', 'l2', 'l3', 'l4', 'l4-1', 'l5']
    step5.rollback_all()
    assert l == []
    list1 = ['l6', 'l7']
    last_step = None
    for item in list1:
        step6 = CompensatingTransaction(
            run_func=add_item,
            run_args=(item,),
            rollback_func=sub_item,
            rollback_args=(item,),
            previous=step5 if not last_step else last_step,
        )
        last_step = step6
        try:
            step6.run()
        except Exception:
            step6.rollback_all(True)
    assert l == []
```