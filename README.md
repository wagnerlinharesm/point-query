# Projeto AWS Lambda com RDS e Secrets Manager

Este projeto detalha o processo de deploy de um ambiente AWS utilizando Terraform, integrando AWS RDS (PostgreSQL) com funções AWS Lambda. O objetivo é realizar consultas a um banco de dados PostgreSQL hospedado na AWS, usando credenciais armazenadas de forma segura e acessíveis via AWS Secrets Manager.

## Componentes

- AWS RDS (PostgreSQL): Serviço de banco de dados relacional para armazenar e recuperar dados.
- AWS Lambda: Serviço de computação sem servidor para executar código em resposta a eventos.
- AWS IAM: Serviço de gerenciamento de acesso para controlar permissões.
- AWS Secrets Manager: Serviço para gerenciar, acessar e armazenar segredos de forma segura.

## Requisitos

- Conta AWS
- AWS CLI configurado
- Terraform
- Python 3.x

## Configuração e Deploy

### Passo 1: Preparação do Ambiente
- Clone o repositório e navegue até o diretório do projeto.
- Configure suas credenciais AWS para acesso programático.

### Passo 2: Terraform

1. Inicialização:

Execute terraform init para inicializar o diretório do Terraform, instalar os provedores requeridos e preparar a configuração.

2. Planejamento:

Com terraform plan, revise as alterações que serão aplicadas no seu ambiente AWS.

3. Aplicação:

Execute terraform apply para criar os recursos na AWS conforme definido nos arquivos de configuração do Terraform.

### Passo 3: Configuração do AWS Lambda

- A função Lambda point_query_lambda_function é configurada para acessar o RDS via VPC, utilizando credenciais armazenadas no Secrets Manager.
- As políticas IAM permitem que a função acesse recursos específicos e executem ações como leitura de segredos e escrita em logs.

### Passo 4: GitHub Actions para CI/CD

- O pipeline CI/CD definido no arquivo de GitHub Actions automatiza o processo de deploy, incluindo configuração de credenciais AWS, inicialização do Terraform, planejamento e aplicação das mudanças, e captura de outputs relevantes.

### Funcionamento

A função Lambda point_query_lambda_function é disparada por eventos definidos (e.g., HTTP requests via Amazon API Gateway), executando a lógica de consulta ao banco de dados utilizando credenciais seguras. A função manipula o evento de entrada, realiza a consulta ao banco de dados RDS utilizando informações de conexão do Secrets Manager e retorna o resultado da consulta.

### Segurança

- As credenciais do banco de dados são armazenadas de forma segura no AWS Secrets Manager.
- A função Lambda opera dentro de uma VPC, garantindo isolamento e segurança na comunicação com o RDS.
- Políticas de IAM restritas garantem o mínimo privilégio necessário para a operação da solução.

### Manutenção e Monitoramento

- Utilize o Amazon CloudWatch para monitorar as invocações da função Lambda e visualizar logs.
- Revise e atualize as políticas de IAM e configurações do Secrets Manager conforme necessário para manter a segurança.

Este projeto demonstra uma implementação segura e eficiente para operações de banco de dados na AWS, utilizando práticas modernas de infraestrutura como código e computação sem servidor.