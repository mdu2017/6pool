mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"2017mark@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]\n\
base = \"dark\"\n\
primaryColor = \"#F63366\"\n\
backgroundColor = \"#0E1117\"\n\
secondaryBackgroundColor = \"#31333F\"\n\
textColor = \"#FAFAFA\"\n\
font = \"serif\"\n\
" > ~/.streamlit/config.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml