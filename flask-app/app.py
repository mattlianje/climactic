from flask import Flask, render_template, json, request, redirect, url_for
from flaskext.mysql import MySQL
import json
import secrets

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = secrets.user
app.config['MYSQL_DATABASE_PASSWORD'] = secrets.password
app.config['MYSQL_DATABASE_DB'] = secrets.db
app.config['MYSQL_DATABASE_HOST'] = secrets.host
mysql.init_app(app)


def retrieveUnlabelledClips(count):
  query = """ SELECT url, start, end FROM labelled
              WHERE completed = FALSE
              ORDER BY RAND()
              LIMIT {:} """.format(count)
  try:
    # connect to db 
    conn = mysql.connect()
    cur = conn.cursor()
    # call select query
    cur.execute(query)
    data = cur.fetchall()
    # close connection
    cur.close()
    conn.close()
    return data
  except Exception as e:
    return { error_msg: 'Error occured retrieving clips', error: e }


def formatYoutubeEmbedUrl(url, start, end):
  embed_url = url.replace("watch?v=", "embed/")
  params = "?start={:}&end={:}&autoplay=1".format(start, end)
  return embed_url + params


@app.route("/", methods=['GET'])
def index():
  if request.method == "GET":
    clips = retrieveUnlabelledClips(1)
    embed_url = ''
    if len(clips) == 0:
      return 'No more clips to label'
    for clip in clips:
      url, start, end = clip
      embed_url = formatYoutubeEmbedUrl(url, start, end)
    return render_template('index.html', embedUrl= embed_url, youtubeUrl= url, start= start, end= end)


def formatAddLabelQuery(url, start, end, data):
  commentator = data['commentator']
  crowd = data['crowd']
  gameplay = data['gameplay']

  query = """ UPDATE labelled
              SET
                commentator = {:},
                crowd = {:},
                gameplay = {:},
                completed = TRUE,
                updated_at = NOW()
              WHERE url = '{:}'
              AND start = {:}
              AND end = {:} """.format(commentator, crowd, gameplay, url, start, end)
  return query


def formatFormInput(formData):
  try:
    if formData['shortcut']:
      inputText = formData['shortcut']
      inputNum = int(inputText)
      
      if inputNum < 111 or inputNum > 332:
        return {'error': 'incorrrect values'}
      
      commentator = inputNum // 100
      crowd = (inputNum % 100) // 10
      gameplay = inputNum % 10

      data = {
        'commentator': commentator - 1,
        'crowd': crowd - 1,
        'gameplay': gameplay - 1,
      }
    else:
      if 'commentator' not in formData or 'crowd' not in formData or 'gameplay' not in formData:
        return {'error': 'missing values'}

      data = {
        'commentator': int(formData['commentator']),
        'crowd': int(formData['crowd']),
        'gameplay': int(formData['gameplay']),
      }
    return data
  except Exception as e:
    return {'error': e}


def validateFormInput(data):
  if 'error' in data:
    return data
  
  if not (0 <= data['commentator'] <= 2):
    data['error'] = 'commentator excitement val must be btwn 1 and 3'
    return data

  if not (0 <= data['crowd'] <= 2):
    data['error'] = 'crowd excitement val must be btwn 1 and 3'
    return data
  
  if not (0 <= data['gameplay'] <= 1):
    data['error'] = 'gameplay val must be btwn 1 and 2'
    return data
  
  return data


@app.route("/addLabel", methods=['POST'])
def addLabel():
  try:
    url = request.form['youtubeUrl']
    start = request.form['start']
    end = request.form['end']

    data = formatFormInput(request.form)
    validatedData = validateFormInput(data)
    # re-render with error msg if error
    if 'error' in validatedData:
      error = validatedData['error']
      embed_url = formatYoutubeEmbedUrl(url, start, end)
      return render_template('index.html', embedUrl= embed_url, youtubeUrl= url, start= start, end= end, error= error)
    
    # connect to db 
    conn = mysql.connect()
    cur = conn.cursor()
    # call update query
    query = formatAddLabelQuery(url, start, end, data)
    cur.execute(query)
    conn.commit()
    # close connection
    cur.close()
    conn.close()

  except Exception as e:
    return json.dumps({'error': str(e)})
  
  return redirect(url_for('index')) #redirecting to home


def formatInsertQuery(data):
  rows = []
  for clip in data:
    url = clip['youtubeUrl']
    start = clip['start']
    end = clip['end']
    rows.append("('{:}', {:} , {:})".format(url, start, end))
  
  query = "INSERT INTO labelled(url, start, end) VALUE {:}".format(",".join(rows))
  return query


@app.route("/addClips", methods=['POST'])
def addClips():
  if request.method == "POST":
    try:
      data = json.loads(request.data)
      # extract data from request
      if data and data['items']:
        new_rows = data['items']
        # connect to db 
        conn = mysql.connect()
        cur = conn.cursor()
        # call insert query
        query = formatInsertQuery(new_rows)
        cur.execute(query)
        conn.commit()
        # close connection
        cur.close()
        conn.close()
        return 'success'
    except Exception as e:
      return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run()
