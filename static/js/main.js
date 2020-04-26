function validate_build_selection()
{
    const build_file = document.getElementById('build_file')
    const build_file_dropdown = document.getElementById('build_files')
	if (build_file.files.length > 0 || build_file_dropdown.value != "")
	{
		return true;
	}
	else
	{
        alert('Please Upload a Build or Select from dropdown');
		return false;
	}
}