mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"2017mark@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
primaryColor=#F63366\n\
backgroundColor=#fafafa\n\
secondaryBackgroundColor=#F0F2F6\n\
textColor=#262730\n\
font=sans serif\n\
" > ~/.streamlit/config.toml