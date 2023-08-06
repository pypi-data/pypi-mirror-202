# Copyright 2021 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.protobuf.empty_pb2 import Empty
from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.sip.sip_pb2 import (
    EndCallRequest,
    PlayWavFilesRequest,
    RegisterAccountRequest,
    SipStatus,
    SipStatusHistoryResponse,
    StartCallRequest,
    StartSessionRequest,
    TransferCallRequest,
)
from ondewo.sip.sip_pb2_grpc import SipStub


class Sip(BaseServicesInterface):
    """
    Exposes the sip endpoints of ONDEWO sip in a user-friendly way.

    See sip.proto.
    """

    @property
    def stub(self) -> SipStub:
        stub: SipStub = SipStub(channel=self.grpc_channel)
        return stub

    def start_session(self, request: StartSessionRequest) -> SipStatus:
        response: SipStatus = self.stub.StartSession(request)
        return response

    def end_session(self) -> SipStatus:
        response: SipStatus = self.stub.EndSession(Empty())
        return response

    def register_account(self, request: RegisterAccountRequest) -> SipStatus:
        response: SipStatus = self.stub.RegisterAccount(request)
        return response

    def start_call(self, request: StartCallRequest) -> SipStatus:
        response: SipStatus = self.stub.StartCall(request)
        return response

    def end_call(self, request: EndCallRequest) -> SipStatus:
        response: SipStatus = self.stub.EndCall(request)
        return response

    def transfer_call(self, request: TransferCallRequest) -> SipStatus:
        response: SipStatus = self.stub.TransferCall(request)
        return response

    def get_sip_status(self) -> SipStatus:
        response: SipStatus = self.stub.GetSipStatus(Empty())
        return response

    def get_sip_status_history(self) -> SipStatusHistoryResponse:
        response: SipStatusHistoryResponse = self.stub.GetSipStatusHistory(Empty())
        return response

    def play_wav_files(self, request: PlayWavFilesRequest) -> SipStatus:
        response: SipStatus = self.stub.PlayWavFiles(request)
        return response

    def mute(self) -> SipStatus:
        response: SipStatus = self.stub.Mute(Empty())
        return response

    def un_mute(self) -> SipStatus:
        response: SipStatus = self.stub.UnMute(Empty())
        return response
