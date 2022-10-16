import pandas as pd
import streamlit as st

from ..services.gensim_service import GensimService


class GensimView:
    title: str = 'Gensim Service'

    gensim_service = GensimService()

    def main(self):

        st.title(self.title)

        with st.expander(label='List', expanded=True):
            st.table(
                pd.DataFrame(
                    self.gensim_service.model_keyword_list).head(200))
            st.write(len(self.gensim_service.model_keyword_list))

        if st.button(label='Calc'):
            self.gensim_service.main()

        st.table(self.gensim_service.most_similar_list)
        st.write(
            f'Positive: {self.gensim_service.random_positive_list[self.gensim_service.random_positive_idx]}')
        st.write(
            f'Negative: {self.gensim_service.random_negative_list[self.gensim_service.random_negative_idx]}')

        with st.form(key='pinterest_service_form'):
            # select_query: str = st.selectbox(label='Select Query', options=pinterest_service.query_list)
            query: str = st.text_input(label='Negative Word')
            # num_pins: int = st.slider('Num of Images', 0, 100, 25)
            submitted = st.form_submit_button(label='Answer')

        if 0 != len(query) and submitted:
            with st.spinner('Wait for it...'):
                is_correct_answer: bool = self.gensim_service.is_correct_answer(
                    word=query)

                if is_correct_answer:
                    st.success('Correct!')
                elif not is_correct_answer:
                    st.warning('Not Correct...')
