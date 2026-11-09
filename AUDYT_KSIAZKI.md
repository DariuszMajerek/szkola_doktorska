# Audyt książki — 9 listopada 2026

Zakres obejmuje wstęp oraz wykłady 1–6 w konfiguracji Quarto Book: definicje, kod analiz, interpretacje wyników, tabele, wygenerowane wykresy, pliki HTML i zgodność z publikacją GitHub Pages. Przejrzano także dwa schematy SVM.

## Ustalenia i poprawki

| Obszar | Ustalenie i rozwiązanie |
|---|---|
| ROC i publikacja | W chwili rozpoczęcia audytu publiczny HTML i PNG ROC były identyczne z lokalnymi plikami: zawierały pięć progów i podpis `1-Specyficzność`. Serwer zwracał `Cache-Control: max-age=600`. Nie potwierdza to stanu pamięci przeglądarki czytelnika. Dodano wersjonowanie adresów wszystkich obrazów na podstawie skrótu ich zawartości, wykonywane po każdym renderowaniu. |
| ROC — obliczenia | Współrzędne wykresu są teraz jawnie wyznaczane jako FPR = 1 − specyficzność i TPR = czułość. Dodano tabelę progów 0,3–0,7, jednoznaczny opis klasy dodatniej i reguły `p >= próg`. Osie mają zakres 0–1, a linia odniesienia łączy (0,0) z (1,1). |
| ROC — testy | Kod porównuje współrzędne z ręcznie obliczonymi odsetkami. Osobny test porównuje AUC z wynikiem opartym na rangach, sprawdza pięć punktów i etykiet, przekątną oraz zgodność progu 0,5 z macierzą pomyłek. |
| Wykład 1 | Dodano rzeczywisty wynik modelu bazowego przewidującego średnią treningową. Doprecyzowano podpis tabeli łączącej dopasowanie pełnego modelu i ocenę predykcji modelu treningowego. Liczba predyktorów ma typ całkowity. Ograniczono nieuzasadnione stwierdzenie o użyteczności każdego predyktora. |
| Wykład 2 | Sprawdzono kodowanie klasy dodatniej, ilorazy szans, hipotezy LRT, stopnie swobody, macierz pomyłek i oba wykresy liniowości logitu. Ocena klasyfikacji i AUC nadal są wyraźnie opisane jako wyniki na danych dopasowania, a nie walidacja na nowych porodach. |
| Wykład 3 | Wizualizacja i podziały zastępcze korzystają dokładnie z workflow ocenionego przez `last_fit()`, zamiast ponownego dopasowania. Do oceny testowej dodano kappę, stosowaną też przy strojeniu. Doprecyzowano ważenie nieczystości przy wyborze podziału i odróżniono pomijanie brakujących współrzędnych na wykresach od zachowania wszystkich wierszy do modelowania. Zwiększono rozmiar rysunku drzewa. |
| Wykład 4 | Ważność cech pochodzi z dokładnie tych modeli, które oceniono na teście. Wyjaśniono mapowanie `min_n` na `min_child_weight` XGBoost i znaczenie Gain. Odróżniono uśrednianie w baggingu/lesie od sumowania w boostingu. Dodano jednostki powierzchni, poprawiono etykiety stanu technicznego i wyjaśnienie transformacji logarytmicznej. |
| Wykład 5 | `kernlab` domyślnie skaluje także cel w regresji. Ustawiono jawnie `scaled = FALSE`, ponieważ predyktory skaluje recepta; `margin` ma teraz jednoznacznie jednostki logarytmu ceny i oznacza połowę szerokości pasa. Wyjaśniono, że schemat pasa tolerancji nie jest dopasowaniem SVR. |
| Wykład 6 | Naprawiono położenie opcji podpisu wykresu aktywacji, jednostkę osi predykcji i komentarz o optymalizatorze. Usunięto sprzeczne z wykresem twierdzenie o systematycznym spadku obu strat; wyjaśniono różne tryby dropout/BatchNorm. Doprecyzowano logit i prawdopodobieństwo klasy 1, skorygowano zbyt kategoryczny opis MSE oraz dodano ograniczenie cen w California Housing. |

| Układ strony | W przeglądarce wykryto, że długie równanie modelu logistycznego rozszerzało całą stronę poza szerokość okna. Dodano przewijanie poziome wyłącznie w obszarze równania. |

## Odtwarzalne kontrole

```sh
Rscript tests/check_roc.R
python3 -m unittest discover -s tests -p 'test_*.py'
quarto render
python3 scripts/verify_book.py
```

Renderowanie wykonuje analizy ze zmienionych źródeł. Przy zmianach wyłącznie w `R/setup.R` należy wymusić wykonanie kodu przez `quarto render --execute`, ponieważ `freeze: auto` nie gwarantuje wykrycia zmiany zewnętrznego pliku.

`verify_book.py` sprawdza komplet siedmiu stron, lokalne odnośniki, istnienie obrazów i ich wersje, nadmierną precyzję komórek tabel, pięć progów ROC, zgodność FPR ze specyficznością, obecność obu wykresów logitu, zapis polskich znaków i składnię bloków Python. Składnię bloków R sprawdzono przez `knitr::purl()` i `parse()`.

## Dokumentacja odniesienia

- [pROC: osie w ggroc](https://search.r-project.org/CRAN/refmans/pROC/html/ggroc.html).
- [kernlab: domyślne skalowanie x i y](https://rdrr.io/cran/kernlab/man/ksvm.html).
- [parsnip: mapowanie parametrów XGBoost](https://parsnip.tidymodels.org/reference/details_boost_tree_xgboost.html).
- [XGBoost: min_child_weight](https://xgboost.readthedocs.io/en/stable/parameter.html).
- [scikit-learn: California Housing](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset).

## Granice oceny

Audyt sprawdza poprawność przedstawionej procedury i zgodność opisów z kodem i wynikami; nie zastępuje zewnętrznej walidacji modeli. Pozostają opisane w książce ograniczenia małej próby `mtcars`, selekcji modelu na tych samych danych w regresji logistycznej, losowych podziałów pingwinów i danych przestrzennych oraz retransformaty logarytmu ceny. Ocena przydatności klinicznej lub przenoszenia modeli na inne populacje wymaga odrębnych danych i projektu badania.

## Wynik wykonania kontroli

- Pełne renderowanie wszystkich rozdziałów zakończyło się powodzeniem.
- Test ROC potwierdził zgodność AUC z rachunkiem rangowym, pięciu punktów i etykiet z progami oraz macierzy pomyłek dla progu 0,5.
- Kontrola HTML objęła siedem stron i 1861 komórek tabel; wszystkie lokalne odnośniki i wersje obrazów są poprawne, bez nadmiernej liczby miejsc po przecinku.
- Dwa testy wersjonowania obrazów przeszły poprawnie: zmiana zawartości zmienia adres, ponowne wykonanie jest idempotentne, a brak obrazu zatrzymuje publikację.
- W przeglądarce sprawdzono wykład 2 przy szerokości 1200 i 390 pikseli: obrazy ładują się, tabela zawiera pięć progów, a strona nie wymaga przewijania poziomego jako całość.
- Po renderowaniu automatycznie usuwane są nieużywane pliki wykresów, które mogły zostać skopiowane ze starszych wyników Quarto.
