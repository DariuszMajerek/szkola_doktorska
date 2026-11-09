# Przegląd i korekty wykładów (28 października 2026)

Zakres: sześć rozdziałów `wyk1.qmd`–`wyk6.qmd`, włączonych do książki w `_quarto.yml`. Starsze pliki `w1.qmd`–`w4.qmd` nie należą do tej edycji książki i nie były objęte korektą merytoryczną.

| Materiał | Znaleziony problem i wprowadzona korekta |
|---|---|
| Wszystkie rozdziały R | W zapisanym HTML polskie litery w tabelach miały postać `<U+0142>` itp. Dodano `R/setup.R`: wybór dostępnego locale UTF-8 przed generowaniem wyników i urządzenie `ragg_png`, jeśli dostępne. Wyniki trzeba odtworzyć, a nie tylko ponownie opakować stary cache. |
| Wykład 1 | Brak odrzucenia normalności przedstawiano jako spełnienie założenia. Teraz rozróżniamy błędy i reszty, wskazujemy ograniczenia testu i rolę Q–Q. |
| Wykład 1 | Panel liniowości wykazuje kształt U, nie uzasadnia zatwierdzenia modelu. Dodano interpretację kierunku błędów, ostrożność wobec heteroskedastyczności, analizę wrażliwości na obserwacje wpływowe i HC3. |
| Wykład 1 | Próg Cooka nie uzasadnia automatycznego usuwania danych. Chrysler Imperial i Toyota Corolla wymagają sprawdzenia; dopasowanie po ich pominięciu służy porównaniu, nie wyborowi wygodnej próby. |
| Wykład 1 | AIC i skorygowany R² nie dowodzą przewagi predykcyjnej. Rozdzielono metryki modelu pełnego i treningowego, ograniczenia testu z 10 aut oraz niepewność po wyborze struktury. Doprecyzowano jednostki `hp` i `disp`. |
| Wykład 2 | `p/(1-p)` to szansa, a OR to stosunek dwóch szans. Dodano definicje, zmianę o wiele jednostek i rozróżnienie eksponentowanego wyrazu wolnego od OR. |
| Wykład 2 | Prosta dopasowana do pięciu zagregowanych logitów nie weryfikuje liniowości warunkowej. Zastąpiono ją porównaniem modeli liniowego i splajnowego dla `lwt` i `age`, z wykresem dla ustalonego profilu oraz pasem niepewności. |
| Wykład 2 | Poprawiono definicję dewiancji, zakres AUC, przekątną na wykresie ROC, jawny kierunek ROC, interpretację pseudo-R² oraz ocen treningowych. |
| Wykład 2 | Pokazano stopnie swobody i GVIF skorygowany o wymiar terminu. EPP liczymy dla siedmiu nachyleń, bez wyrazu wolnego; próg 10 nie jest testem założeń. Dodano kontrolę zbieżności, dźwigni, Cooka, separacji i możliwe działania zaradcze. |
| Wykład 2 | LRT `race + age` jest łączny, nie dowodzi wkładu każdej cechy. Usunięto nieuzasadnione oceny znaczenia klinicznego, ograniczono język przyczynowy i dodano przedziały ufności prognozowanych prawdopodobieństw. |
| Wykład 3 | Wyniki foldów nie są niezależnymi powtórzeniami. Usunięto sztywno wpisane wartości metryk. Dodano ograniczenia wniosków o ważności cech, brakach danych i generalizacji między koloniami. |
| Wykład 4 | Algorytm do prezentacji predykcji był wybierany na podstawie testu. Teraz wybór następuje według walidacji treningowej. Wyjaśniono `yardstick::rsq`, błąd retransformaty logarytmu i ograniczenia ważności opartej na nieczystości. |
| Wykład 5 | Epsilon to połowa szerokości pasa, a pas nie jest przedziałem predykcyjnym. Uzupełniono ograniczenia retransformaty, metryki `rsq` i uogólniania wyników. |
| Wykład 6 | Opis odwracał etykiety zbioru `breast_cancer`: w kodzie sklearn `0` oznacza guz złośliwy, `1` łagodny. Dopasowano opis, interpretację sigmoida i fałszywych wyników ujemnych do kodu. |
| Wykład 6 | Dodano wybór epoki według walidacji także w klasyfikacji, doprecyzowano Adam względem SGD i deterministyczny charakter ilustracji Rosenbrocka, ograniczenia ReLU i uniwersalnej aproksymacji. Usunięto twierdzenia o dowiedzionym braku przeuczenia i gwarantowanej trafności. |

## Kontrola wyników

Ponowne obliczenie modeli potwierdziło m.in.:

- regresja liniowa: Shapiro–Wilk p ≈ 0,0713, VIF ≈ 2,54–4,92, maksymalny Cook ≈ 0,270 wobec 4/n = 0,125;
- klasyczny test współczynnika `am`: p ≈ 0,0458; po zastosowaniu HC3 p ≈ 0,0750 — klasyfikacja według progu 0,05 jest wrażliwa na sposób wyznaczenia niepewności;
- regresja logistyczna: AIC modeli kolejno ≈ 233,80; 230,34; 222,83; 219,95;
- łączny LRT dla splajnów `lwt` i `age`: 4 dodatkowe stopnie swobody, p ≈ 0,1355; brak odrzucenia nie potwierdza liniowości;
- 59 zdarzeń / 7 współczynników predyktorów daje EPP ≈ 8,4;
- źródła QMD zapisane są jako UTF-8; składnia wszystkich 16 bloków Python została sprawdzona;
- wszystkie sześć rozdziałów przeszło renderowanie z ponownym wykonaniem kodu; w HTML każdego rozdziału sprawdzono brak zapisów `<U+…>` i znaków zastępczych; obejrzano wygenerowane wykresy diagnostyczne regresji liniowej i liniowości logitu.

## Odtwarzanie

Rozdziały 1–5 wymagają R z pakietami używanymi w kodzie, w tym `ragg`, `sandwich`, `lmtest`, `palmerpenguins`, `rpart.plot`, `kernlab` i pakietami modelowania. Rozdział 6 wymaga Pythona z PyTorch, scikit-learn, matplotlib, pandas, Jupyter i ipykernel. Pobranie California Housing przy pierwszym uruchomieniu wymaga dostępu do sieci.

```sh
quarto render wyk1.qmd --to html --execute
quarto render wyk2.qmd --to html --execute
quarto render wyk3.qmd --to html --execute
quarto render wyk4.qmd --to html --execute
quarto render wyk5.qmd --to html --execute
uv run --with torch --with scikit-learn --with matplotlib --with pandas --with jupyter --with ipykernel quarto render wyk6.qmd --to html --execute
```

`--execute` jest istotne po zmianach wspólnego `R/setup.R`: `freeze: auto` może zachować wyniki rozdziału, którego własne źródło nie zostało zmienione.

Wygenerowana książka znajduje się w `docs/`. Poprawne wykonanie kodu nie jest walidacją naukową modeli ani dowodem ich przydatności poza kontekstem przykładów.

## Prezentacja wyników

Wydruki konsolowe testów, metryk, macierzy pomyłek i strojenia modeli zastąpiono tabelami `gt` w rozdziałach R. Rozdział Python używa tabel HTML `pandas.Styler`. Tabele mają tytuły, uporządkowane nagłówki i formatowanie liczb; wartości p poniżej 0,001 mają osobny zapis. Macierze pomyłek przedstawiają obserwacje w wierszach, a prognozy w kolumnach.

## Aktualizacja 9 listopada 2026

- Ujednolicono tabele wszystkich wykładów do trzech miejsc po przecinku, zachowując liczebności jako liczby całkowite. Małe wartości p są zapisywane jako `< 0,001`, a bardzo małe hiperparametry w notacji naukowej.
- W wykładzie 1 dodano globalny test F wraz z wartością p i interpretacją; uproszczono interpretację testu Shapiro–Wilka.
- W wykładzie 2 poprawiono oś i linię odniesienia ROC, oznaczono progi 0,3–0,7 i dodano osobne wykresy liniowości logitu dla masy ciała i wieku matki. Usunięto zbędne sekcje i odniesienia do miar wyłączonych z prezentacji.
- W wykładzie 3 usunięto kodowanie dummy dla CART. Zachowano oryginalne braki danych, pokazano podziały zastępcze oraz predykcje dla obserwacji z brakami.
- Usunięto końcowe podsumowania dydaktyczne z wykładów 1, 2, 4 i 5.
- Cała książka została wyrenderowana; kontrola 1559 komórek tabel w sześciu rozdziałach nie wykazała wyników z nadmierną liczbą miejsc po przecinku.
