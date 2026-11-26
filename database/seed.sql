INSERT INTO kategori (nama_kategori) VALUES
('Pupuk'),
('Pestisida'),
('Benih');

INSERT INTO role (nama_role) VALUES 
('admin'), 
('petugas'), 
('petani');

INSERT INTO users (nama, username, password, no_hp, alamat, status, id_role) VALUES
('rendra gemoy', 'rendra_admin', 'admin123', '08111111111', 'Desa Sukosari, Bondowoso', true, 1),
('Achmad Firdaus', 'Fir_punkoioi', 'petugas123', '082222222222', 'antah berantah', true, 2),
('Firda Amelia', 'firdaamel', 'amel123', '083333333333', 'antah berantah', true, 3),
('Bilqis Retno', 'Bilqis_Cuek', 'qis123', '08444444444', 'antah berantah', true, 3);

INSERT INTO pemasok (nama_pemasok, no_hp, alamat) VALUES
('CV Tani Makmur', '082111111111', 'Jl. Raya Surabaya No. 10'),
('PT Agro Subur', '082222222223', 'Jl. Industri No. 25, Malang'),
('UD Sumber Pertanian', '082333333333', 'Jl. Pasar Baru No. 3, Jember');

INSERT INTO barang (nama_barang, harga, satuan, stok, batas_minimum, id_kategori, id_pemasok) VALUES
('Pupuk Urea', 2800, 'kg', 5000, 1000, 1, 1),
('Pupuk NPK', 3600, 'kg', 3000, 750, 1, 2),
('Insektisida Decis', 85000, 'liter', 30, 10, 2, 3),
('Fungisida Antracol', 95000, 'kg', 8, 10, 2, 2),
('Benih Padi Ciherang', 15000, 'kg', 50, 10, 3, 1);

INSERT INTO permintaan (jumlah, keperluan, tanggal, status, id_users, id_barang) VALUES
(250, 'Pemupukan sawah 1 hektar', '2026-11-01', 'disetujui', 3, 1),
(2, 'Penyemprotan hama wereng', '2026-11-03', 'menunggu', 4, 3),
(10, 'Tanam padi musim hujan', '2026-11-05', 'disetujui', 3, 5);

INSERT INTO transaksi (jenis_transaksi, tanggal, id_users, id_permintaan) VALUES
('masuk', '2026-10-28', 2, NULL),
('masuk', '2026-10-30', 2, NULL),
('keluar', '2026-11-02', 2, 1),
('keluar', '2026-11-06', 2, 3);

INSERT INTO detail_transaksi (jumlah, harga_satuan, tgl_kadaluwarsa, sisa, id_barang, id_transaksi) VALUES
(2500, 2750, '2027-10-28', 2250, 1, 1),
(30, 15000, '2027-04-30', 20, 5, 1),
(30, 85000, '2027-12-31', 30, 3, 1),
(8, 95000, '2027-09-30', 8, 4, 1),
(3000, 3550, '2028-10-30', 3000, 2, 2),
(2750, 2750, '2028-10-28', 2750, 1, 2),
(30, 15000, '2027-08-31', 30, 5, 2),
(250, 2800, '2027-10-28', NULL, 1, 3),
<<<<<<< HEAD
(10, 15000, '2027-04-30', NULL, 5, 4);
=======
(10, 15000, '2027-04-30', NULL, 5, 4);
>>>>>>> 9f9b4d32c89fc570a23441156943dc4d2540d370
