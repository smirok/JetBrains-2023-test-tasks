package org.example.matching;

import org.junit.jupiter.api.Test;
import org.opentest4j.AssertionFailedError;

import java.time.Duration;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.*;

class RegexMatcherTest {

    private static boolean matches(String text, String regex) {
        return Pattern.compile(regex).matcher(text).matches();
    }

    @Test
    void matchesWithStackOverflowError() {
        String text = "ab".repeat(10000);
        String regex = "^(((a|b)*)+)*$";
        assertFalse(RegexMatcher.matches(text, regex));
        assertThrowsExactly(StackOverflowError.class, () -> RegexMatcherTest.matches(text, regex));
    }

    @Test
    void matchesWithTimeout() {
        String text = "ac".repeat(10000);
        String regex = "^(([abc]*)+)A$";
        assertFalse(RegexMatcher.matches(text, regex));
        assertThrowsExactly(
                AssertionFailedError.class,
                () -> assertTimeout(Duration.ofSeconds(5), () -> RegexMatcherTest.matches(text, regex))
        );
    }
}
