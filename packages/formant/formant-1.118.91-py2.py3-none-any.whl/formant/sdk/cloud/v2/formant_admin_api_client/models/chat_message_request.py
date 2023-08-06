from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tool_description import ToolDescription


T = TypeVar("T", bound="ChatMessageRequest")


@attr.s(auto_attribs=True)
class ChatMessageRequest:
    """
    Attributes:
        message (str):
        default_prompt_template (str):
        tool_choice_prompt (str):
        tools (List['ToolDescription']):
        idea_suggestion_prompt (str):
        max_tokens (Union[Unset, float]):
        frequency_penalty (Union[Unset, float]):
        presence_penalty (Union[Unset, float]):
        temperature (Union[Unset, float]):
        top_p (Union[Unset, float]):
    """

    message: str
    default_prompt_template: str
    tool_choice_prompt: str
    tools: List["ToolDescription"]
    idea_suggestion_prompt: str
    max_tokens: Union[Unset, float] = UNSET
    frequency_penalty: Union[Unset, float] = UNSET
    presence_penalty: Union[Unset, float] = UNSET
    temperature: Union[Unset, float] = UNSET
    top_p: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        default_prompt_template = self.default_prompt_template
        tool_choice_prompt = self.tool_choice_prompt
        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()

            tools.append(tools_item)

        idea_suggestion_prompt = self.idea_suggestion_prompt
        max_tokens = self.max_tokens
        frequency_penalty = self.frequency_penalty
        presence_penalty = self.presence_penalty
        temperature = self.temperature
        top_p = self.top_p

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "defaultPromptTemplate": default_prompt_template,
                "toolChoicePrompt": tool_choice_prompt,
                "tools": tools,
                "ideaSuggestionPrompt": idea_suggestion_prompt,
            }
        )
        if max_tokens is not UNSET:
            field_dict["maxTokens"] = max_tokens
        if frequency_penalty is not UNSET:
            field_dict["frequencyPenalty"] = frequency_penalty
        if presence_penalty is not UNSET:
            field_dict["presencePenalty"] = presence_penalty
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["topP"] = top_p

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tool_description import ToolDescription

        d = src_dict.copy()
        message = d.pop("message")

        default_prompt_template = d.pop("defaultPromptTemplate")

        tool_choice_prompt = d.pop("toolChoicePrompt")

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = ToolDescription.from_dict(tools_item_data)

            tools.append(tools_item)

        idea_suggestion_prompt = d.pop("ideaSuggestionPrompt")

        max_tokens = d.pop("maxTokens", UNSET)

        frequency_penalty = d.pop("frequencyPenalty", UNSET)

        presence_penalty = d.pop("presencePenalty", UNSET)

        temperature = d.pop("temperature", UNSET)

        top_p = d.pop("topP", UNSET)

        chat_message_request = cls(
            message=message,
            default_prompt_template=default_prompt_template,
            tool_choice_prompt=tool_choice_prompt,
            tools=tools,
            idea_suggestion_prompt=idea_suggestion_prompt,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            temperature=temperature,
            top_p=top_p,
        )

        chat_message_request.additional_properties = d
        return chat_message_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
