package com.example.wepapelima.model;

import jakarta.validation.constraints.NotNull;

public record UpdateElementRequest(
        @NotNull Integer oldElement,
        @NotNull Integer newElement
) {
}
