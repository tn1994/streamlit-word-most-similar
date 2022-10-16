import logging

import streamlit as st

from .base_view import spinner_wrapper
# from .gensim_view import GensimView
from .magnitude_view import MagnitudeView
from ..services.version_service import VersionService

logger = logging.getLogger(__name__)


class Sidebar:

    def __init__(self):
        self.service_dict = {
            # 'gensim_service': self.gensim_service,
            'magnitude_service': self.magnitude_service,
            'version_service': self.version_service,
        }

    def main(self):
        radio_value = st.sidebar.radio('Sub Page', self.service_dict.keys())
        if radio_value:
            select_service = self.service_dict[radio_value]
            select_service()

    @staticmethod
    def gensim_service():
        gensim_view = GensimView()
        gensim_view.main()

    @staticmethod
    @spinner_wrapper
    def magnitude_service():
        magnitude_view = MagnitudeView()
        magnitude_view.main()

    @spinner_wrapper
    def version_service(self):
        st.title('Version Service')
        version_service = VersionService()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label='Python Version',
                      value=version_service.get_python_version())
        with c2:
            st.metric(
                label='Pip Version',
                value=version_service.get_pip_version())
        with c3:
            st.metric(
                label='Streamlit Version',
                value=version_service.get_library_version(
                    library_name='streamlit'))
        st.download_button(label='Download requirements.txt',
                           data=version_service.get_pip_list(format='freeze'),
                           file_name='requirements.txt',
                           mime='text/txt')
        pip_list = version_service.get_pip_list(format='json')
        with st.expander('Pip List', expanded=True):
            st.table(pip_list)
