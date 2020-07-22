from SpiffWorkflow.bpmn.serializer.BpmnSerializer import BpmnSerializer
from SpiffWorkflow.bpmn.serializer.Packager import Packager

from SpiffWorkflow.bpmn.specs.BpmnProcessSpec import BpmnProcessSpec
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow

packager_file = '/Users/abin/code/LipotesOps/lipotes-b/Test.bpmn20.zip'
packager = Packager(packager_file, entry_point_process='主机上架')
bpmn_file = '/Users/abin/code/LipotesOps/lipotes-b/Test.bpmn20.xml'

packager.add_bpmn_file(bpmn_file)
packager.create_package()

packager_data = open(packager_file, 'rb').read()
serializer = BpmnSerializer()

wf_spec = serializer.deserialize_workflow_spec(packager_data, filename=packager_file)
wf = BpmnWorkflow(wf_spec)

wf.dump()
step = 0
while True:
    step=step+1
    print(step)
    if(wf.complete_next()):
        wf.dump()
        continue
    break
pass
