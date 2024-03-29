import json
import csv
import io


def build():
    submit_map = {}
    with io.open('./submit/submit.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['sid', 'recommend_mode', 'probability_list'])
        with open('./out/normed_test_session.txt', 'r') as f1:
            with open('./testres/res0', 'r') as f2:
                cur_session =''
                for x, y in zip(f1.readlines(), f2.readlines()):
                    m1 = json.loads(x)
                    session_id = m1["session_id"]
                    if cur_session == '':
                        cur_session = session_id

                    transport_mode = m1["plan"]["transport_mode"]

                    if cur_session != session_id:
                        writer.writerow([str(cur_session), str(submit_map[cur_session]["transport_mode"]),
                                         json.dumps(submit_map[cur_session]['probability_list'])])
                        cur_session = session_id
                    if session_id not in submit_map:
                        submit_map[session_id] = {}
                        submit_map[session_id]['probability_list'] = {}
                        submit_map[session_id]["transport_mode"] = transport_mode
                        submit_map[session_id]["probability"] = float(y)
                        submit_map[session_id]['probability_list'][transport_mode] = float(y)
                        #if int(submit_map[session_id]["transport_mode"]) == 0 and submit_map[session_id]["probability"] > 0.02:
                            #submit_map[session_id]["probability"] = 0.99
                    else:
                        submit_map[session_id]['probability_list'][transport_mode] = float(y)
                        if float(y) > float(submit_map[session_id]["probability"]):
                            submit_map[session_id]["transport_mode"] = transport_mode
                            submit_map[session_id]["probability"] = float(y)
                            #if int(submit_map[session_id]["transport_mode"]) == 0 and submit_map[session_id]["probability"] > 0.02:
                                #submit_map[session_id]["transport_mode"] = 0
                                #submit_map[session_id]["probability"] = 0.99


        writer.writerow([str(cur_session), str(submit_map[cur_session]["transport_mode"]), json.dumps(submit_map[cur_session]['probability_list'])])



if __name__ == "__main__":
    build()
