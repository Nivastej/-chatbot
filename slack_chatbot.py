
slack_verification_token=os.environ["SLACK_VERIFICATION_TOKEN"]

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

print ("""""")

@app.route('/', methods=["GET", "POST"])
def webhook():



    if request.method == 'GET':
        location_code="2 (slack token)"
        print (app_code,location_code, "method is GET at ", datetime.utcnow())
        print (app_code,location_code, "received get request, starting get process")
        open_db_connection(app_code,location_code)
     

        print (app_code,location_code,"successfully got token, finishing process and shutting down")


      
        return auth_complete
 

    if request.method == 'POST':
       
        location_code="3 (received POST)"
        print (app_code,location_code," method is POST at ", datetime.utcnow()," post process started")

      
        post_request = request.get_json(silent=True, force=True)

        if not post_request:
            
            button_message(app_code,location_code,request)
            return make_response("", 200)

    
        print (app_code,location_code," got json")
        print (app_code,location_code,"post_request: ", post_request)



        if "challenge" in post_request:
            
            location_code="3.1 (Slack challenge)"
            print (app_code,location_code," challenge detected")

        
            response_to_challenge=challenge_response(app_code,location_code,post_request)

            print (app_code,location_code," response_to_challenge: ",response_to_challenge )

            print (app_code,location_code,"success, sending challenge response")


            return response_to_challenge

        else:
            

            location_code="4.1 (Slack user message)"
            print (app_code,location_code," know it isn't challange at ", datetime.utcnow())

            if "event" in post_request:
                
                print (app_code,location_code," slack event")

               
                post_request_data=post_request.get("event")
                print (app_code,location_code," have got event")

                
                print (app_code,location_code," post_request_data", post_request_data)
                
                bot_id=post_request_data.get("bot_id")
                if bot_id:
                    location_code="4.1.1 (bot message)"
                    print (app_code,location_code," picking up bot message, id: ", bot_id)
                    print (app_code, location_code, "shutting down")

                    return make_response("Bot message", 200)
                   

                location_code="4.2 (getting info)"


                user_id=post_request_data.get("user")
                print (app_code,location_code," user_id: ", user_id)

               
                query=post_request_data.get("text")
                print (app_code,location_code," query: ", query)

                
                event_id=post_request.get("event_id")
                print (app_code,location_code," event id: ", event_id)

               
                channel=post_request_data.get("channel")
                print (app_code,location_code," channel: ", channel)


               

                location_code="4.3 (send async)"

                print (app_code,location_code," sending to worker")
                tasks.send_to_api(event_id, user_id, channel, query)

            
            
                return make_response("Passed to API", 200)

                

def get_token(app_code,location_code):


    sublocation="A (get_token) - "
    print(app_code,location_code,sublocation,"token received")
    print(app_code,location_code,sublocation," request referrer: ",request.headers.get("Referer"))
    print(app_code,location_code,sublocation," starting post install")


    auth_code = request.args['code']
    print (app_code,location_code,sublocation," auth code: ", auth_code)

    
    sc = SlackClient("")

   
    auth_response = sc.api_call(
    "oauth.access",
    client_id=client_id,
    client_secret=client_secret,
    code=auth_code
    )

    print(app_code,location_code,sublocation,"auth response: ",auth_response)
    print(app_code,location_code,sublocation,"app access token",auth_response['access_token'])
    print(app_code,location_code,sublocation,"bot access token",auth_response['bot']['bot_access_token'])

 


    print(app_code,location_code,sublocation," printing authorisation response: ", auth_response)


    source="Slack" #This is hard coded for now but could be changed based on where the authorisation request comes from
    user_id=auth_response['user_id']
    user_token= auth_response['access_token']
    bot_token= auth_response['bot']['bot_access_token']
    team_id= auth_response['team_id']
    team_name= auth_response['team_name']
    channel=auth_response['incoming_webhook']['channel_id']



 
    print (app_code,location_code,sublocation," done user_creator process")

    speech_to_send='Hi, thanks for adding Vietnambot! If you ever want to add an order to the Vietnamese sheet just write that food in this channel or say "I want [food]" and I\'ll add it. For reference the sheet is located at: '+google_sheet_url

    
    params = (
    ('token', user_token),
    ('channel', channel),
    ('text', speech_to_send),
    ('username', 'vietnambot'),
    ('icon_emoji', ':ramen:'),
    ('pretty', '1'),
    )
    requests.get('https://slack.com/api/chat.postMessage', params=params)

    print (app_code,location_code,sublocation,"sent to Slack, finishing process")

  
  


def challenge_response(app_code,location_code,post_request):

    sublocation="B (challenge_response) - "
    print (app_code,location_code,sublocation,"post_request is", post_request)



    print(app_code,location_code,sublocation," challenge in slack event, creating response")
    return make_response(post_request["challenge"], 200, {"content_type":"application/json"})


def open_db_connection(app_code,location_code):
    sublocation="C (open_db_connection) - "
    print (app_code,location_code,sublocation," starting setting up database connection")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    
    print (app_code,location_code,sublocation," url: ", url)


    global conn

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )



   
    global cur
    cur = conn.cursor()



    print (app_code,location_code,sublocation," finishing setting up database connection")

    return



def close_db_connection(app_code,location_code):
        sublocation="D (close_db_connection) - "

        print (app_code,location_code,sublocation," starting connection shut down")

        #Closing connection with database
        cur.close()
        print (app_code,location_code,sublocation," closed cursor")
        conn.close()
        print (app_code,location_code,sublocation," closed connection")

        print (app_code,location_code,sublocation," finished connection shut down")
        return




def user_creator(app_code,location_code,source, user_id, user_token, bot_token, team_id, team_name):

    sublocation="E (user_creator)"

    print (app_code,location_code,sublocation," creating user process")
    print (app_code,location_code,sublocation, " source: ", source, " user_id: ", user_id, " user_token: ", user_token, " bot_token: ", bot_token," team_id: ", team_id," team_name: ", team_name)

    

    print (app_code,location_code,sublocation," trying to fetch all tables")
    cur.execute("""SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public'""")
    for table in cur.fetchall():
        print (app_code,location_code,sublocation,table)

  
    print (app_code,location_code,sublocation,"success, trying to fetch all rows in users_and_actions")
    cur.execute("SELECT * FROM users_and_actions LIMIT 0")
    print (app_code,location_code,sublocation," successful fetch")
    colnames = [desc[0] for desc in cur.description]
    print (app_code,location_code,sublocation," columns in table are: ", colnames)

    
    cur.execute("SELECT user_token FROM users_and_actions WHERE user_id = %(uid)s",{"uid": user_id})
    existing_token=cur.fetchone()

    print (app_code,location_code,sublocation," existing_token is ", existing_token)



    if existing_token!=None:
       
        print (app_code,location_code,sublocation," user already created")
        cur.execute("SELECT * FROM users_and_actions WHERE user_id = %(uid)s",
                   {"uid": user_id})
        print (app_code,location_code,sublocation," web user_creator - fetching one result: ", cur.fetchone())
        print (app_code,location_code,sublocation," web user_creator - end of function")
        return

      

    cur.execute("INSERT INTO users_and_actions (source, user_id, user_token, bot_token, team_id, team_name) VALUES (%s, %s, %s, %s, %s, %s);", (source, user_id, user_token, bot_token, team_id, team_name))

    print (app_code,location_code,sublocation," added ", user_id, " to users_and_actions")
    
    conn.commit()
    print (app_code,location_code,sublocation," committed ",user_id," data")


    
    print (app_code,location_code,sublocation," recalling ", user_id, " only")
    cur.execute("SELECT user_id FROM users_and_actions WHERE user_id = %(uid)s",
               {"uid": user_id})
    print (app_code,location_code,sublocation," fetching new user ID: ", cur.fetchone())
    print (app_code,location_code,sublocation," recalling whole record")
    cur.execute("SELECT * FROM users_and_actions WHERE user_id = %(uid)s",
               {"uid": user_id})
    print (app_code,location_code,sublocation," fetching one result: ", cur.fetchone())
    print (app_code,location_code,sublocation," end of function")

    return



def update_columns(app_code,location_code,list_of_pairs, user_id):


    sublocation="F (update_columns)"

    print (app_code,location_code,sublocation," starting update_columns process")
    print (app_code,location_code,sublocation," defining column is user_id")
    print (app_code,location_code,sublocation," defining value is: ", user_id)



    print (app_code,location_code,sublocation," retrieving values before change")
   
    cur.execute("SELECT * FROM users_and_actions WHERE user_id = %s", (user_id,));

    print (app_code,location_code,sublocation," values as they are: ", cur.fetchone())

   

    print (app_code,location_code,sublocation,"splitting list_of_pairs into update_pairs")

   
    update_pairs = [list_of_pairs[x:x+2] for x in range(0, len(list_of_pairs), 2)]
    print (app_code,location_code,sublocation,"list split into update_pairs")

    for pair in update_pairs:
        print (app_code,location_code,sublocation," splitting the column, value pair to acess column and value separately")
        print (app_code,location_code,sublocation," first pair is: ", pair)

       
        column=pair[0]
        print (app_code,location_code,sublocation," column to update is ", column)

       
        values_to_add= pair[1]
        print (app_code,location_code,sublocation," value to add to ", column, " is ", values_to_add)

        

        cur.execute("UPDATE users_and_actions SET "+column+"=%s WHERE user_id=%s", (values_to_add, user_id));

       
        updated_rows = cur.rowcount
        print (app_code,location_code,sublocation," number of rows updated = ", updated_rows)
        conn.commit()
        print (app_code,location_code,sublocation," committed data")
        print (app_code,location_code,sublocation," executed change, updated users_and_actions column: ", column, "to be ", values_to_add ," where user_id is ", user_id)
        cur.execute("SELECT "+ column +" FROM users_and_actions WHERE user_id= %s", (user_id,));
        print(app_code,location_code,sublocation," value after most recent change: ", cur.fetchone())

       

    print(app_code,location_code,sublocation," retrieving values after change")
    cur.execute("SELECT * FROM users_and_actions WHERE user_id= %s", (user_id,));
    print(app_code,location_code,sublocation," values as they are post change: ", cur.fetchone())
    print(app_code,location_code,sublocation," end of function")

    print(app_code,location_code,sublocation," ending update_columns process")

    return
def check_database(app_code,location_code,user_id, column):
 
    sublocation="G (check_database)"

    print (app_code,location_code,sublocation,"starting check_database process, user_id is: ", user_id)

    
    cur.execute("SELECT "+column+" FROM users_and_actions WHERE user_id = %(current_uid)s",{"current_uid": user_id})
    value=cur.fetchone()

    print (app_code,location_code,sublocation," ending check_database process")

    for item in value:
         print (app_code,location_code,sublocation," ",column," is: ", item_to_use)
        
 
    return item_to_use


def button_message(app_code,location_code,request):
    sublocation="H (interactive button)"

    
    form_json = json.loads(request.form["payload"])

    print (app_code,location_code,sublocation," request is: ", form_json)

    
    selection=form_json.get('actions')[0].get('value')
    print (app_code,location_code,sublocation," selection is: ", selection)

    user_id=form_json.get('user').get('id')
    print (app_code,location_code,sublocation," user is: ", user_id)

    channel=form_json.get('channel').get('id')
    print (app_code,location_code,sublocation," channel is: ", channel)

    
    query=selection

    event_id="button_push"

    tasks.send_to_api(event_id, user_id, channel, query)

    return



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    
