Qual o funcionamento?

-> Alimente o arquivo teste.csv (você pode renomer) com os CNJP's que deseja consultar, linha a linha.
-> Execute o programa no terminal e informe como primeiro parametro o path desse arquivo csv.
	Ex: python consulta_receita_AWS.py teste.csv
-> É verificado um CNPJ a cada 20 segundos, respeitando as limitações de requisição da API da receita.
-> Verifique a pasta e verá um arquivo com diversas informações de cada CNPJ, linha a linha.
	-> Se o CNPJ estiver errado ou simplesmente não for possível consultar a segunda coluna irá conter a mensagem de erro.
	-> Caso queira adicionar informações ou até retirar você deve alterar a função consulting_aws().
	