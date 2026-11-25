DROP TABLE IF EXISTS detail_transaksi, transaksi, permintaan, barang,
                     pemasok, users, role, kategori CASCADE;
DROP TYPE IF EXISTS jenis_role, jenis_satuan;

CREATE TYPE jenis_role AS ENUM ('admin', 'petugas', 'petani');
CREATE TYPE jenis_satuan AS ENUM ('kg', 'gram', 'liter', 'ml', 'sachet', 'pcs');

CREATE TABLE kategori (
    id_kategori   SERIAL PRIMARY KEY,
    nama_kategori VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE role (
    id_role   SERIAL PRIMARY KEY,
    nama_role jenis_role NOT NULL UNIQUE
);

CREATE TABLE users (
    id_users SERIAL PRIMARY KEY,
    nama     VARCHAR(100) NOT NULL,
    username VARCHAR(50)  NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    no_hp    VARCHAR(15)  NOT NULL UNIQUE,
    alamat   TEXT NOT NULL,
    status   BOOL NOT NULL DEFAULT TRUE,
    id_role  INT NOT NULL REFERENCES role(id_role)
);

CREATE TABLE pemasok (
    id_pemasok   SERIAL PRIMARY KEY,
    nama_pemasok VARCHAR(100) NOT NULL UNIQUE,
    no_hp        VARCHAR(15)  NOT NULL UNIQUE,
    alamat       TEXT NOT NULL
);

CREATE TABLE barang (
    id_barang     SERIAL PRIMARY KEY,
    nama_barang   VARCHAR(100) NOT NULL,
    harga         DECIMAL(12,2) NOT NULL,
    satuan        jenis_satuan NOT NULL,
    stok          INTEGER NOT NULL DEFAULT 0,
    batas_minimum INTEGER NOT NULL,
    id_kategori   INT NOT NULL REFERENCES kategori(id_kategori),
    id_pemasok    INT NOT NULL REFERENCES pemasok(id_pemasok)
);

CREATE TABLE permintaan (
    id_permintaan SERIAL PRIMARY KEY,
    jumlah        INTEGER NOT NULL,
    keperluan     VARCHAR(255) NOT NULL,
    tanggal       DATE NOT NULL,
    status        VARCHAR(20) NOT NULL DEFAULT 'menunggu',
    id_users      INT NOT NULL REFERENCES users(id_users),
    id_barang     INT NOT NULL REFERENCES barang(id_barang)
);

CREATE TABLE transaksi (
    id_transaksi    SERIAL PRIMARY KEY,
    jenis_transaksi VARCHAR(20) NOT NULL,
    tanggal         DATE NOT NULL,
    id_users        INT NOT NULL REFERENCES users(id_users),
    id_permintaan   INT REFERENCES permintaan(id_permintaan)
);

CREATE TABLE detail_transaksi (
    id_detail       SERIAL PRIMARY KEY,
    jumlah          INTEGER NOT NULL,
    harga_satuan    DECIMAL(12,2) NOT NULL,
    tgl_kadaluwarsa DATE,
    sisa            INTEGER,
    id_barang       INT NOT NULL REFERENCES barang(id_barang),
    id_transaksi    INT NOT NULL REFERENCES transaksi(id_transaksi)
);
