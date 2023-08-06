from pdb import set_trace as stop
import json
class GraphDB():
  @staticmethod
  def query_fsm(mqtt_client, fsm_uid):
    query = """{
      result(func: uid(%s))
      {
        fsm_tag
        name
        name@zh
        init_state
        description
        state {
          uid
          fsm_tag
          name
          name@zh
          description
          on_entry @facets {
            uid
            name
            name@zh
            topic
            description
          }
          on_exit @facets {
            uid
            name
            name@zh
            topic
            description
          }
          transit @facets {
            uid
            fsm_tag
            name
            name@zh
          }
        }
        variable {
          uid
          fsm_tag
          name
          name@zh
          dtype
          default
          persistent
          description
        }
        transition {
          uid
          name
          name@zh
          fsm_tag
          description
          event {
            uid
            fsm_tag
            name
            name@zh
            topic
            condition
          }
        }
        action {
          uid
          name
          name@zh
          fsm_tag
          description
          topic
          act_type
          input @facets{
            uid
          }
          output @facets{
            uid
          }
          input_key
          output_key
        }
        event {
          uid
          fsm_tag
          fsm_id
          description
          name
          name@zh
          topic
          output @facets{
            ~output { uid }
            uid
          }
          output_key
        }
      }
      }""" % (fsm_uid)
    data = json.dumps({"query": query})
    stop()
    res = mqtt_client.publish_request('/graph/devices/01/selectors/query', data, qos = 1, timeout = 5)
    return res