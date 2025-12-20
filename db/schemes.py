def schemes():
    user = """
        create table user (
        id bigint primary key generated always as identity,
        nombre text not null,
        apellido text not null,
        telefono text not null,
        correo text not null unique
    );"""

    login="""
        create table login (
        id bigint primary key generated always as identity,
        usuario_id bigint not null,
        password text not null,
        foreign key (usuario_id) references usuario (id)
    );"""

    user_test="""
        create table usuario_test (
        usuario_id bigint not null,
        test_id bigint not null,
        primary key (usuario_id, test_id),
        foreign key (usuario_id) references usuario (id),
        foreign key (test_id) references test (id)
    );"""