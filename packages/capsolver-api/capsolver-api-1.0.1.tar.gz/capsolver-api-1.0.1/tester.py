import capsolver_py

capsolver = capsolver_py.HCaptchaTask('CAI-4B81C259F4CB60E4B9A33EDAA0D483ED')

print(capsolver.get_balance())

task_id = capsolver.create_task(task_type='HCaptchaTaskProxyLess',
                                website_url='https://accounts.hcaptcha.com/demo',
                                website_key='a5f74b19-9e45-40e0-b45d-47ff91b7a6c2',
                                is_invisible=True,
                                enable_ipv6=False,
                                enterprise_payload={'rqdata': 'blabla'},
                                proxy='blabla',
                                user_agent='blabla'
                                )

print(capsolver.get_solution(task_id))

