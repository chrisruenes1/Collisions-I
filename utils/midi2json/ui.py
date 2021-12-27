def confirm(prompt, valid_responses):
    awaiting_confirmation = True
    while awaiting_confirmation:
        response = input(prompt)
        if (response in valid_responses):
            awaiting_confirmation = False
            return response
        else:
            print('invalid response')

def confirm_entry(confirm_entries_prompt, get_data_fn):
    response = None
    while response_negative(response):
        response = confirm(
            f'{confirm_entries_prompt}. Confirm? y/n', ['y', 'n'])
        if (response_negative(response)):
            get_data_fn()
        else:
            return True

def response_negative(response):
    return response in ['n', None]