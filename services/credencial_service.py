import uuid

import keyring

from repositories.credencial_repository import (
    CredencialRepository,
)


SERVICO_KEYRING = "RPA_FISCAL_ASSISTIDO"


URLS_SISTEMAS = {
    "TOTVS": "http://192.168.5.71:5000/webapp/",
    "GISS ONLINE": "https://diadema.giss.com.br/portal/home#/login-portal",
}


class CredencialService:

    def __init__(self):

        self.repository = (
            CredencialRepository()
        )

    def listar(self):

        return (
            self.repository.listar()
        )

    def salvar(
        self,
        sistema,
        tipo_vinculo,
        usuario,
        senha,
        empresa_id=None,
        filial_id=None,
    ):

        sistema = (
            sistema.strip().upper()
        )

        tipo_vinculo = (
            tipo_vinculo.strip().upper()
        )

        usuario = (
            usuario.strip()
        )

        senha = (
            senha.strip()
        )

        if not sistema:

            raise ValueError(
                "Selecione o sistema."
            )

        if sistema not in URLS_SISTEMAS:

            raise ValueError(
                (
                    "Sistema não configurado "
                    "para automação."
                )
            )

        if tipo_vinculo not in {
            "GLOBAL",
            "ESTABELECIMENTO",
        }:

            raise ValueError(
                "Tipo de vínculo inválido."
            )

        if not usuario:

            raise ValueError(
                "Informe o usuário / CPF."
            )

        if not senha:

            raise ValueError(
                "Informe a senha."
            )

        if (
            tipo_vinculo
            == "ESTABELECIMENTO"
            and not filial_id
        ):

            raise ValueError(
                "Selecione o estabelecimento."
            )

        if tipo_vinculo == "GLOBAL":

            empresa_id = None
            filial_id = None

        chave_cofre = (
            f"{sistema}_"
            f"{uuid.uuid4().hex}"
        )

        keyring.set_password(
            SERVICO_KEYRING,
            chave_cofre,
            senha,
        )

        try:

            credencial = (
                self.repository.criar(
                    sistema=sistema,
                    tipo_vinculo=tipo_vinculo,
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                    usuario=usuario,
                    chave_cofre=chave_cofre,
                )
            )

        except Exception:

            try:

                keyring.delete_password(
                    SERVICO_KEYRING,
                    chave_cofre,
                )

            except Exception:
                pass

            raise

        return credencial

    def obter_para_execucao(
        self,
        sistema,
        filial_id=None,
    ):

        sistema = (
            sistema.strip().upper()
        )

        if sistema not in URLS_SISTEMAS:

            raise ValueError(
                (
                    f"O sistema '{sistema}' "
                    "não possui URL configurada."
                )
            )

        if filial_id:

            credencial = (
                self.repository
                .buscar_por_estabelecimento(
                    sistema=sistema,
                    filial_id=filial_id,
                )
            )

            if credencial:

                return self._montar_acesso(
                    credencial
                )

        credencial = (
            self.repository
            .buscar_global(
                sistema
            )
        )

        if credencial:

            return self._montar_acesso(
                credencial
            )

        return None

    def obter_url(
        self,
        sistema,
    ):

        sistema = (
            sistema.strip().upper()
        )

        url = URLS_SISTEMAS.get(
            sistema
        )

        if not url:

            raise ValueError(
                (
                    f"Não existe URL configurada "
                    f"para {sistema}."
                )
            )

        return url

    def _montar_acesso(
        self,
        credencial,
    ):

        senha = keyring.get_password(
            SERVICO_KEYRING,
            credencial.chave_cofre,
        )

        if senha is None:

            raise RuntimeError(
                (
                    "A credencial existe no banco, "
                    "mas a senha não foi localizada "
                    "no cofre do Windows."
                )
            )

        url = self.obter_url(
            credencial.sistema
        )

        return {
            "id": credencial.id,
            "sistema": credencial.sistema,
            "url": url,
            "usuario": credencial.usuario,
            "senha": senha,
            "tipo_vinculo": credencial.tipo_vinculo,
            "empresa_id": credencial.empresa_id,
            "filial_id": credencial.filial_id,
        }
