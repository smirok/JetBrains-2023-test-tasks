package com.example.wepapelima.model;

import jakarta.validation.constraints.NotNull;

public record RemoveElementRequest(
        @NotNull Integer oldElement
) {
}
