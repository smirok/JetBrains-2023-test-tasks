package com.example.wepapelima.model;


import jakarta.validation.constraints.NotNull;

public record InsertElementRequest(
        @NotNull Integer newElement
) {
}
