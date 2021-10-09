from abc import ABC
from dataclasses import dataclass

from django.db import models
from rest_framework import serializers


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SerilizerNone(serializers.Serializer):
    pass


@dataclass(init=False)
class Result:
    __create_key = object()
    __is_success: bool
    __error_message: str

    def __init__(self, create_key, success: bool, error_message: str):
        assert (
            create_key == Result.__create_key
        ), "OnlyCreatable objects must be created using OnlyCreatable.create"
        self.__error_message = error_message
        self.__is_success = success

    @classmethod
    def failure(cls, error_message: str):
        return Result(cls.__create_key, False, error_message)

    @classmethod
    def success(cls):
        return Result(cls.__create_key, True, "")

    @property
    def is_failure(self) -> bool:
        return not self.__is_success

    @property
    def error_message(self) -> str:
        if self.is_failure:
            return self.__error_message
        return ""
