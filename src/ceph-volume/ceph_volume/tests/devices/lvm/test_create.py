import pytest
from ceph_volume.devices import lvm


class TestCreate(object):

    def test_main_spits_help_with_no_arguments(self, capsys):
        lvm.create.Create([]).main()
        stdout, stderr = capsys.readouterr()
        assert 'Create an OSD by assigning an ID and FSID' in stdout

    def test_main_shows_full_help(self, capsys):
        with pytest.raises(SystemExit):
            lvm.create.Create(argv=['--help']).main()
        stdout, stderr = capsys.readouterr()
        assert 'Use the filestore objectstore' in stdout
        assert 'Use the bluestore objectstore' in stdout
        assert 'A physical device or logical' in stdout

    def test_excludes_filestore_bluestore_flags(self, is_root):
        with pytest.raises(RuntimeError) as error:
            lvm.create.Create(argv=['--data', '/dev/sdvv', '--filestore', '--bluestore']).main()
        expected = 'Cannot use --filestore (filestore) with --bluestore (bluestore)'
        assert expected in str(error)

    def test_excludes_other_filestore_bluestore_flags(self, is_root):
        with pytest.raises(RuntimeError) as error:
            lvm.create.Create(argv=[
                '--bluestore', '--data', '/dev/sdvv',
                '--journal', '/dev/sf14',
            ]).main()
        expected = 'Cannot use --bluestore (bluestore) with --journal (filestore)'
        assert expected in str(error)

    def test_excludes_block_and_journal_flags(self, is_root):
        with pytest.raises(RuntimeError) as error:
            lvm.create.Create(argv=[
                '--bluestore', '--data', '/dev/sdvv', '--block.db', 'vg/ceph1',
                '--journal', '/dev/sf14',
            ]).main()
        expected = 'Cannot use --block.db (bluestore) with --journal (filestore)'
        assert expected in str(error)
