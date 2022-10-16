import uuid
import pandas as pd
import streamlit as st
from typing import Final

from ..services.magnitude_service import MagnitudeService


class MagnitudeView:
    title: Final[str] = 'Magnitude Service'

    key_1: Final[str] = str(uuid.uuid1())
    key_2: Final[str] = str(uuid.uuid1())

    magnitude_service = MagnitudeService()

    def __init__(self):
        self.service_dict = {
            'what_negative_word_service': self.what_negative_word_service,
            'what_positive_word_service': self.what_positive_word_service,
            'other_services': self.other_services,
        }

    def main(self):
        st.title(self.title)

        page_value = st.sidebar.selectbox(
            label='Sub Service', options=self.service_dict.keys())
        if page_value:
            select_service = self.service_dict[page_value]
            select_service()

    def what_negative_word_service(self):
        with st.expander(label='List', expanded=True):
            # st.table(pd.DataFrame(self.magnitude_service.model_keyword_list)[0].head(200))
            st.metric(label='Num of Model Words', value=len(
                self.magnitude_service.model_keyword_list))

        col1, col2 = st.columns([.3, .7])

        with col1:
            with st.form(key='magnitude_service_form'):
                st.write(
                    f'Positive: {self.magnitude_service.random_positive_list[self.magnitude_service.random_positive_idx]}')
                st.write(
                    f'Negative: {self.magnitude_service.random_negative_list[self.magnitude_service.random_negative_idx]}')
                # select_query: str = st.selectbox(label='Select Query', options=pinterest_service.query_list)
                query: str = st.text_input(label='Negative Word')
                # num_pins: int = st.slider('Num of Images', 0, 100, 25)
                submitted = st.form_submit_button(label='Answer')

            if 0 != len(query) and submitted:
                with st.spinner('Wait for it...'):
                    is_correct_answer: bool = self.magnitude_service.is_correct_answer(
                        word=query)

                    if is_correct_answer:
                        st.success('Correct!')
                    elif not is_correct_answer:
                        st.warning('Not Correct...')

        with col2:
            if st.button(label='Calc'):
                with st.spinner('Wait for it...'):
                    self.magnitude_service.main()

            st.table(self.magnitude_service.most_similar_list)

    def what_positive_word_service(self):
        with st.expander(label='List', expanded=True):
            # st.table(pd.DataFrame(self.magnitude_service.model_keyword_list)[0].head(200))
            st.metric(label='Num of Model Words', value=len(
                self.magnitude_service.model_keyword_list))

        col1, col2 = st.columns([.3, .7])

        with col1:
            with st.form(key='magnitude_service_form'):
                st.write(
                    f'Positive: {self.magnitude_service.random_positive_list[self.magnitude_service.random_positive_idx]}')
                st.write(
                    f'Negative: {self.magnitude_service.random_negative_list[self.magnitude_service.random_negative_idx]}')
                # select_query: str = st.selectbox(label='Select Query', options=pinterest_service.query_list)
                query: str = st.text_input(label='Negative Word')
                # num_pins: int = st.slider('Num of Images', 0, 100, 25)
                submitted = st.form_submit_button(label='Answer')

            if 0 != len(query) and submitted:
                with st.spinner('Wait for it...'):
                    is_correct_answer: bool = self.magnitude_service.is_correct_answer(
                        word=query)

                    if is_correct_answer:
                        st.success('Correct!')
                    elif not is_correct_answer:
                        st.warning('Not Correct...')

        with col2:
            if st.button(label='Calc'):
                with st.spinner('Wait for it...'):
                    self.magnitude_service.main()

            st.table(self.magnitude_service.most_similar_list)

    def other_services(self):
        self._query_most_similar()
        self._query_word_using_vector()

    def _query_most_similar(self):
        with st.form(key=self.key_1):
            # positive_word: str = st.selectbox(label='Positive', options=self.magnitude_service.random_positive_list)
            # negative_word: str = st.selectbox(label='Negative', options=self.magnitude_service.random_negative_list)
            positive_word: str = st.text_input(label='Positive')
            negative_word: str = st.text_input(label='Negative')
            submitted = st.form_submit_button(label='Query')

        if 0 not in (len(positive_word), len(negative_word)) and submitted:
            with st.spinner('Wait for it...'):
                result: list = self.magnitude_service.query_most_similar(
                    positive=positive_word, negative=negative_word)

                if result:
                    st.table(pd.DataFrame(result)[0])

    def _query_word_using_vector(self):
        with st.form(key=self.key_2):
            vectors: str = st.text_input(label='Vectors')
            submitted = st.form_submit_button(label='Query')

        if 0 not in (len(vectors),) and submitted:
            with st.spinner('Wait for it...'):
                result: list = self.magnitude_service.get_word_using_vector(
                    vectors=vectors)

                if result:
                    st.table(result)
