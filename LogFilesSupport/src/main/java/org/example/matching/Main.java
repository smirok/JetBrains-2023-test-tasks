package org.example.matching;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

class RegexMatcher {

    public static boolean matches(String text, String regex) {
        java.util.regex.Matcher matcher = Pattern.compile(regex).matcher(text);
        CompletableFuture<Boolean> completableFuture = CompletableFuture.supplyAsync(matcher::matches);

        try {
            return completableFuture.completeOnTimeout(false, 5, TimeUnit.SECONDS).get();
        } catch (InterruptedException | ExecutionException e) {
            return false;
        }
    }
}

public class Main {

    public static void main(String[] args) {
    }
}
