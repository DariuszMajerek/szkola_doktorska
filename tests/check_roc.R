# Sprawdzenie kodu wykładu i niezależne odtworzenie współrzędnych ROC.
source("R/setup.R")
blok <- function(etykieta) {
  linie <- readLines("wyk2.qmd", encoding = "UTF-8")
  start <- which(linie == paste0("#| label: ", etykieta))
  stopifnot(length(start) == 1L)
  koniec <- start + which(linie[(start + 1L):length(linie)] == "```")[1L]
  parse(text = linie[(start + 1L):(koniec - 1L)])
}
for (etykieta in c("wyk2-przygotowanie", "wyk2-modele-kandydackie")) {
  eval(blok(etykieta))
}
model_koncowy <- model_4
eval(blok("wyk2-macierz-pomylek"))
wykres <- eval(blok("wyk2-roc-progi"))
y <- dane_model$low01
p <- dane_model$pred_prob
n1 <- sum(y == 1)
n0 <- sum(y == 0)
auc_z_rang <- (sum(rank(p)[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0)
stopifnot(abs(as.numeric(pROC::auc(roc_obj)) - auc_z_rang) < 1e-12)
warstwy <- ggplot2::ggplot_build(wykres)$data
indeks <- function(klasa) which(vapply(wykres$layers, function(w) inherits(w$geom, klasa), logical(1)))
punkty <- warstwy[[indeks("GeomPoint")]]
etykiety <- warstwy[[indeks("GeomLabelRepel")]]
przekatna <- warstwy[[indeks("GeomSegment")]]
stopifnot(
  nrow(punkty) == 5L,
  isTRUE(all.equal(punkty$x, progi_roc$fpr)),
  isTRUE(all.equal(punkty$y, progi_roc$sensitivity)),
  nrow(etykiety) == 5L,
  all(progi_roc$etykieta %in% etykiety$label),
  przekatna$x == 0, przekatna$y == 0,
  przekatna$xend == 1, przekatna$yend == 1,
  wykres$labels$x == "1-Specyficzność (FPR)",
  wykres$labels$y == "Czułość (TPR)"
)
punkt_05 <- progi_roc[progi_roc$threshold == 0.5, ]
stopifnot(
  abs(punkt_05$sensitivity - tabela_pomylek["niska", "niska"] / sum(y == 1)) < 1e-12,
  abs(punkt_05$fpr - tabela_pomylek["prawidłowa", "niska"] / sum(y == 0)) < 1e-12
)
cat("OK: AUC z rang, pięć progów ROC, współrzędne wykresu i macierz pomyłek.\n")
