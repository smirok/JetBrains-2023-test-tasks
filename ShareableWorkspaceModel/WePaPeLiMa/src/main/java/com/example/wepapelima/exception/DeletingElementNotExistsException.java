package com.example.wepapelima.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(code = HttpStatus.UNPROCESSABLE_ENTITY, reason = "oldElement doesn't exists in the last version!")
public class DeletingElementNotExistsException extends RuntimeException {
}
