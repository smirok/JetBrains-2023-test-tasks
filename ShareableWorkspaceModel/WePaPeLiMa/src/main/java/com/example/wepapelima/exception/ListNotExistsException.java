package com.example.wepapelima.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(code = HttpStatus.NOT_FOUND, reason = "This version of list doesn't exists!")
public class ListNotExistsException extends RuntimeException {
}
