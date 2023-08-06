r'''
Parsers are used to parse the output from OpenAI into the right format. The purpose of the paraser is to
 parse the new output and append it to the prepared_data. Every parser will receive:
    - data: the new data output from OpenAI for one example
    - prepared_data: the dataset we are creating, in other words old data that was output by a parser
    - prompt_config: the prompt_config for the current prompt as a dictionary (taken from the .yaml file)
    - config: general config, ie the whole .yaml file as a python-box 
    - row: the row from the original CSV that was used for context to generate the `data`, can be empty given the use-case
    - raw_data_id: the ID of the `data` in the raw_data CSV (used to store the raw output from OpenAI)
    - prompt_text: the prepared prompt that was used to generate `data`

If we are running the paraser for the first time the `prepared_data` will be empty (None) and it is up to us to define how that CSV (dataframe) should look,
and what columns should it have. Every parser can have different columns depending on the use-case.
'''


import pandas as pd
from io import StringIO
import re
import logging

def csv_parser(data, prepared_data, prompt_config, config, row, raw_data_id, prompt_text):
    r''' Parse CSV output from OpenAI, the output will be appened to `prepared_data` if it is not None, and returned.
    '''
    qa_pairs = None
    df = pd.read_csv(StringIO(data), sep=';;;;', engine='python')

    # Strip everything
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    ref_col = prompt_config.get('reference_column_to_append', None)
    if ref_col and ref_col in row and row[ref_col]:
        # Means we want to append a reference at the end of each Answer
        to_append = f"\nReferences:\n- {row[ref_col]}"
        df['Answer'] = df['Answer'] + to_append
    df['Question'] += f' {config.special_tokens.eos}' # Every Q/A pair is independent
    df['Answer'] += f' {config.special_tokens.eos} {config.special_tokens.eod}'
    qa_pairs = [f'{config.special_tokens.user} {q.strip()} {config.special_tokens.ai} {a.strip()}' for q,a in df[['Question', 'Answer']].values]

    new_data = pd.DataFrame([[text, raw_data_id] for text in qa_pairs], columns=['text', 'raw_data_id'])
    if prepared_data is None:
        prepared_data = new_data
    else:
        prepared_data = pd.concat([prepared_data, new_data], ignore_index=True)

    return prepared_data


def medical_conversation_parser(data, prepared_data, prompt_config, row, config, raw_data_id, prompt_text):
    conversation = None

    # Merge the extractions into one conversation
    data = re.split(r'\s*(Patient:|AI-Assistant:)\s*', data)[1:]
    if len(data) > 0:
        conversation = ""
        to_append = None

        ref_col = prompt_config.get('reference_column_to_append', None)
        if ref_col and ref_col in row and row[ref_col]:
            # Means we want to append a reference at the end of each Answer
            to_append = f"\nReferences:\n- {row[ref_col]}"

        actor = None
        for message in data:
            message = message.strip()
            if message in ['Patient:', 'AI-Assistant:']:
                actor = message
            elif actor is not None: 
                if actor == 'Patient:':
                    conversation += f'{config.special_tokens.user} {message} {config.special_tokens.eos} '
                elif actor == 'AI-Assistant:':
                    conversation += f'{config.special_tokens.ai} {message}'
                    if to_append is not None and to_append:
                        conversation += to_append
                    conversation += f" {config.special_tokens.eos} "
        if conversation:
            conversation = conversation.strip() + f" {config.special_tokens.eod}"

    new_data = pd.DataFrame([[conversation, raw_data_id]], columns=['text', 'raw_data_id'])
    if prepared_data is None:
        prepared_data = new_data
    else:
        prepared_data = pd.concat([prepared_data, new_data], ignore_index=True)

    return prepared_data