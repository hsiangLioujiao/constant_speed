import streamlit as st
from github import Github
from github import Auth


github_repo_name = "constant_speed"

# https://docs.streamlit.io/develop/api-reference/connections/st.secrets
token = st.secrets["github"]["token"]

auth = Auth.Token(token)
g = Github(auth=auth)
repo = g.get_user().get_repo(github_repo_name)


def main():
    st.title("檔案上傳並儲存至 GitHub")

    st.subheader("上傳檔案")
    uploaded_file = st.file_uploader("選擇檔案")

    if uploaded_file is not None:
        file_details = {
            "檔名": uploaded_file.name,
            "檔案類型": uploaded_file.type,
            "檔案大小": uploaded_file.size,
        }
        st.write(file_details)
        
        st.subheader("儲存至 GitHub")
        save_button = st.button("將檔案儲存至 GitHub")
        
        if save_button:
            # 將檔案內容讀取為 bytes
            file_content = uploaded_file.read()
            
            # 設定檔案路徑與提交訊息
            file_path = f"uploads/{uploaded_file.name}"
            commit_message = f"新增檔案：{uploaded_file.name}"
            
            try:
                # 如果檔案已存在，更新內容
                contents = repo.get_contents(file_path)
                repo.update_file(file_path, commit_message, file_content, contents.sha)
                st.success(f"檔案 '{uploaded_file.name}' 已成功更新至 GitHub！")
            except:
                # 如果檔案不存在，新增檔案
                repo.create_file(file_path, commit_message, file_content)
                st.success(f"檔案 '{uploaded_file.name}' 已成功新增至 GitHub！")

if __name__ == "__main__":
    main()


g.close()
