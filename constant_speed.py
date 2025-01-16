import streamlit as st
from github import Github
from github import Auth


st.write("test")

# https://docs.streamlit.io/develop/api-reference/connections/st.secrets
token = st.secrets["github"]["token"]

auth = Auth.Token(token)
g = Github(auth=auth)

user = g.get_user()
print("用戶: ", user.login)
st.write(f"用戶: {user.login}")

for repo in user.get_repos():
    print(repo.name)

# To close connections after use
g.close()
