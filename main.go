package main

import (
  "fmt"
  "os"
  "sort"
  "strings"
  "strconv"
  "net/http"
  "io/ioutil"
  "encoding/json"
  "github.com/spf13/viper"
  "github.com/bclicn/color"
  "github.com/olekukonko/tablewriter"
)

func colorize(value string) string {
  if strings.HasPrefix(value, "-") {
    return color.Red(value)
  } else {
    return color.Green(value)
  }
}

type Setting struct {
  Key map[string]interface{}
  OtherField string
}

type Cur_dat struct {
  Id string
  Name string
  Symbol string
  Price_usd string
  Percent_change_1h string
  Percent_change_24h string
  Percent_change_7d string
}

func market_value(currency, fiat string) []Cur_dat {
  url := "https://api.coinmarketcap.com/v1/ticker/" + currency + "/?convert=" + fiat
  resp, err := http.Get(url)

  var mydata []Cur_dat

  if err != nil {
    fmt.Printf("there was an error getting the url\n")
    os.Exit(1)
  } else {
    defer resp.Body.Close()
    contents, err := ioutil.ReadAll(resp.Body) // contents = []byte
    if err != nil {
      fmt.Printf("there was an error reading the response\n")
      panic(err)
    }

    json.Unmarshal([]byte(contents), &mydata)
  }
  return mydata
}

func string_to_float(in_value string) float64 {
  out_value, err := strconv.ParseFloat(in_value, 64)
  if err != nil {
    fmt.Printf("Something happened converting %s to a float\n", in_value)
  }
  return out_value
}

func float_to_string(in_value float64) string {
  out_value := strconv.FormatFloat(in_value, 'f', 8, 64)
  return out_value
}

func float_to_currency(in_value float64) string {
  out_value := strconv.FormatFloat(in_value, 'f', 2, 64)
  return out_value
}

func main() {
  viper.SetConfigName(".heli")
  dir := os.ExpandEnv("${HOME}/")
  viper.AddConfigPath(dir)
  viper.ReadInConfig()

  settings := viper.AllSettings()
  balances := settings["balances"].(map[string]interface{})
  currencies := make([]string, 0, len(balances))

  general := viper.GetStringMapString("general")

  for k := range balances {
    currencies = append(currencies, k)
  }

  sort.Strings(currencies)

  table := tablewriter.NewWriter(os.Stdout)
  table.SetHeader([]string{"Currency", "Price", "Amount", "Balance", "1h", "1d", "1w"})
  table.SetAlignment(tablewriter.ALIGN_RIGHT)
  table.SetBorder(false)
  table.SetCenterSeparator(" ")
  table.SetColumnSeparator(" ")

  var gross float64 = 0

  for _, currency := range currencies {
    currency_data := market_value(currency, general["fiat_currency"])[0]

    price := string_to_float(currency_data.Price_usd)
    amount := balances[currency].(float64)
    balance := float_to_currency(
      string_to_float(currency_data.Price_usd)*amount,
    )
    hour := colorize(currency_data.Percent_change_1h)
    day := colorize(currency_data.Percent_change_24h)
    week := colorize(currency_data.Percent_change_7d)

    gross = gross + string_to_float(currency_data.Price_usd)*amount

    data_line := []string{
      currency,
      float_to_currency(price),
      float_to_string(amount),
      balance,
      hour,
      day,
      week,
    }
    table.Append(data_line)
  }

  exp := string_to_float(general["invested"])
  net := gross+exp

  table.Append([]string{"", "", "", "", "", "", ""})
  table.Append([]string{"", "", "Gross", float_to_currency(gross), "", "", ""})
  table.Append([]string{"", "", "Exp", float_to_currency(exp), "", "", ""})
  table.Append([]string{"", "", "Net", colorize(float_to_currency(net)), "", "", ""})
  table.Render()

  fmt.Printf("All prices displayed in %s.\n", general["fiat_currency"])
  fmt.Printf("Prices sourced from https://coinmarketcap.com.\n")
}
