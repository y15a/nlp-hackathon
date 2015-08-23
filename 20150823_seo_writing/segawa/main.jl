using MeCab
import JSON

mecab = Mecab()

function getCorpus()
  results = Dict{Any, Int64}()
  for gm in eachline(open("../../../data/1gm-0000"))
    result = split(gm, '\t')
    results[result[1]] = int64(result[2])
  end
  results
end

function isNounOrVerb(feature)
  findfirst(["名詞", "動詞"], feature) > 0
end

function isHiragana(word)
  ismatch(r"^[ぁ-ゞ]+", word)
end

println("## Initializing...")
corpus = getCorpus()
println("## Initializing...OK")

for data in JSON.parse(readall(open("../../../data/results.json")))
  dict = Dict{Any, Int64}()

  query = data["query"]
  println("### $(query)")

  for result in data["results"]
    body = result["body"]
    words = parse(mecab, body)

    for word in words
      feature = split(word.feature, ',')
      word_length = length(word.surface)

      # 動詞、名詞以外を排除
      if ! isNounOrVerb(feature[1])
        continue
      end

      # 一文字を排除
      if word_length <= 1
        continue
      end

      # ２文字のひらがなを排除
      if word_length <= 2 && isHiragana(word.surface)
        continue
      end

      # コーパスにない単語を排除
      if ! haskey(corpus, word.surface)
        continue
      end

      # println("++ $(word.surface)[$(length(word.surface))]: $(feature[1]), $(corpus[word.surface])")

      if haskey(dict, word.surface)
        dict[word.surface] += corpus[word.surface]
      else
        dict[word.surface] = corpus[word.surface]
      end
    end
  end

  wordcounts = sort(collect(dict), by = tuple -> last(tuple), rev = true)
  count = 1

  for wordcount in wordcounts
    println("[$(count)] $(wordcount[1]): $(wordcount[2])")
    count += 1; if count > 10; break end
  end

  println("==================\n")
end
