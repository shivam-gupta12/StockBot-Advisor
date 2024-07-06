import matplotlib
matplotlib.use('Agg')
from flask import render_template, request, jsonify, session
from app.services.search_service import get_urls
from app.services.document_service import load_documents, process_documents
from app.services.chat_service import create_chat_logic, ask_question, format_output_to_html
from app.services.query_service import create_query_transformation_logic, transform_query
from app.services.forecast_service import fetch_stock_data , calculate_moving_averages , plot_stock_trends
from app.services.ticker_service import extract_ticker , ticker_extractor

def init_routes(app, socketio):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/process_query', methods=['POST'])
    def process_query():
        original_query = request.json.get('query')  
        print('Query received: ', original_query)
        
        query_transformation_chain = create_query_transformation_logic()
        query = transform_query(query_transformation_chain, original_query)
        print('Transformed Query: ', query)
        
        extractor = ticker_extractor()
        ticker = extractor(original_query)
        print("ticker symbol : " , ticker)
        
        stock_data = fetch_stock_data(ticker=ticker)
        moving_avg_data = calculate_moving_averages(stock_data)
        base64_image = plot_stock_trends(moving_avg_data, ticker)
 
        # region_safe_search = session.get('regionSafeSearch', False)
        # max_results = int(session.get('maxResults', 5))
        # selected_region = session.get('selectedRegion', 'in-en')

        # print('Settings fetched from session:')
        # print('Region SafeSearch:', region_safe_search)
        # print('Max Results:', max_results)
        # print('Selected Region:', selected_region)

        urls = get_urls(query)  
        print('URLs fetched: ', urls)

        docs_list = load_documents(urls)
        retriever = process_documents(docs_list)
        chat_logic_chain = create_chat_logic(retriever)
        answer = ask_question(chat_logic_chain, query)
        print('Answer generated: ', answer)

        formatted_answer = format_output_to_html(answer)
        
        return jsonify({
            'answer': formatted_answer,
            'image_data': base64_image    
        })

