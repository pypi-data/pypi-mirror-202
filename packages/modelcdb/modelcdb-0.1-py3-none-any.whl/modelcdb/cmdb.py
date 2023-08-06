import pymysql
import pickle


def modelcdb(*argv):
    conn = pymysql.connect(host=argv[0], user=argv[1], password=argv[2], db=argv[3], charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    if argv[4] == 'save':
        aimodel=pickle.dumps(argv[5])
        if argv[6]<20 :
            if argv[7]>=80 :
                status=1
            else:
                status=0
        else:
            status=0
        cur.execute("INSERT INTO Prediction_Model (model,status) VALUES (%s,%s)", (aimodel,status))
        conn.commit()
        conn.close()
    elif argv[4] == 'load':
        sql = 'select model from Prediction_Model where status=1 order by history_id desc limit 1;'
        cur.execute(sql)
        DB_model_data = cur.fetchone()
        remodel=pickle.loads(DB_model_data.get('model'))
        conn.close()
        return remodel
    else:
        conn.close()
        return 0
