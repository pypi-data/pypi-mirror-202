from extra_streamlit_tools._logging import logging as logger
import streamlit as st
from typing import Any, Optional


def clear_cache(keep_keys: Optional[list[str]] = None) -> None:
    """
    Resets the Streamlit cache.

    Parameters
    ----------
        keep_keys:Optional[list[str]]
            Keys to not be cleared from cache
    """

    logger.debug("Clearing cache")
    for key in st.session_state.keys():
        if keep_keys is None or key not in keep_keys:
            logger.debug(f"Deleting key: {key}")
            del st.session_state[key]
        else:
            logger.debug(f"Keeping key: {key}")


def init_session_keys(key_value_pairs: dict[str, Any]) -> None:
    """
    The init_session_keys function is a helper function that initializes the session state with keys and values.

    Parameters
    ----------
        key_value_pairs:dict[str, Any]
            A dictionairy of key_value_pairs
    """  # noqa
    for key, value in key_value_pairs.items():
        if key not in st.session_state:
            st.session_state[key] = value


def change_in_session_state(key_value_pairs: dict[str, Any]):
    """
    The change_in_session_state function is a helper function that allows you to change session state values.

    Parameters
    ----------
        key_value_pairs:dict[str, Any]
            Dictionairy with the Streamlit session_state key and the its new value
    """  # noqa
    for key, value in key_value_pairs.items():
        st.session_state[key] = value


def set_selectbox_index(
    selectbox_key: str, session_state_var_name: str, values: list[Any]
) -> None:
    """
    The set_selectbox_index function is a helper function that sets the index of a selectbox to the value
    of another session state variable. This is useful when you want to set the default value of one selectbox
    to be equal to another, but you don't know what that other's default value will be until runtime.

    Parameters
    ----------
        selectbox_key:str
            Specify the key of the selectbox
        session_state_var_name:str
            Set the session state variable name
        values:list[Any]
            The list of values in the selectbox
    """  # noqa
    st.session_state[session_state_var_name] = values.index(
        st.session_state[selectbox_key]
    )
