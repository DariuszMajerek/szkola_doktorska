# knitr uruchamiany w locale C zapisuje polskie litery jako <U+0142> itd.
# Wybieramy dostępną lokalizację UTF-8 przed utworzeniem tabel i wykresów.
if (!isTRUE(l10n_info()[["UTF-8"]])) {
  for (locale_utf8 in c("C.UTF-8", "en_US.UTF-8", "pl_PL.UTF-8")) {
    suppressWarnings(Sys.setlocale("LC_CTYPE", locale_utf8))
    if (isTRUE(l10n_info()[["UTF-8"]])) break
  }
}
if (!isTRUE(l10n_info()[["UTF-8"]])) {
  stop("Renderowanie wymaga dostępnej lokalizacji UTF-8 (LC_CTYPE).")
}
options(encoding = "UTF-8")
knitr::opts_chunk$set(message = FALSE)
if (requireNamespace("ragg", quietly = TRUE)) {
  knitr::opts_chunk$set(dev = "ragg_png")
}

# Wspólny format wszystkich tabel, także tworzonych bezpośrednio przez gt().
formatuj_tabele <- function(tabela) {
  dane <- tabela[["_data"]]
  tabela <- tabela |>
    gt::fmt_number(columns = where(is.double), decimals = 3,
                   dec_mark = ",", sep_mark = " ") |>
    gt::sub_missing(missing_text = "—")
  for (kolumna in intersect(c("p", "p_value", "p.value"), names(dane))) {
    if (!is.numeric(dane[[kolumna]])) next
    tabela <- tabela |> gt::fmt(columns = all_of(kolumna), fns = function(x) {
      ifelse(is.na(x), NA_character_,
             ifelse(x < 0.001, "< 0,001", formatC(x, digits = 3,
                                                 format = "f", decimal.mark = ",")))
    })
  }
  # Małe hiperparametry nie mogą po zaokrągleniu wyglądać jak zero.
  for (kolumna in intersect(c("cost_complexity", "learn_rate", "rbf_sigma"), names(dane))) {
    male <- which(!is.na(dane[[kolumna]]) & dane[[kolumna]] != 0 &
                    abs(dane[[kolumna]]) < 0.001)
    if (length(male)) {
      tabela <- tabela |> gt::fmt_scientific(
        columns = all_of(kolumna), rows = male, decimals = 3, dec_mark = ","
      )
    }
  }
  tabela
}

# Jednolita prezentacja wyników liczbowych zamiast wydruków konsolowych.
tabela_wynikow <- function(dane, tytul) {
  wynik <- gt::gt(as.data.frame(dane)) |>
    formatuj_tabele() |>
    gt::tab_header(title = tytul) |>
    gt::opt_row_striping() |>
    gt::tab_options(table.font.size = gt::px(14),
                    heading.align = "left",
                    column_labels.font.weight = "bold")
  if ("p_value" %in% names(dane)) {
    wynik <- wynik |> gt::cols_label(p_value = "p")
  }
  wynik
}

tabela_pomylek_gt <- function(macierz, tytul) {
  dane_tabeli <- data.frame(Obserwowane = rownames(macierz),
                           as.data.frame.matrix(macierz), check.names = FALSE)
  tabela_wynikow(dane_tabeli, tytul) |>
    gt::tab_spanner(label = "Przewidywana klasa", columns = -Obserwowane) |>
    gt::fmt_integer(columns = -Obserwowane) |>
    gt::tab_source_note("Wiersze: klasa obserwowana; kolumny: klasa przewidywana.")
}
