from django import forms
from .models import Pengiriman

class FormPengiriman(forms.ModelForm):
    class Meta:
        model = Pengiriman
        fields = ['nama_pelanggan', 'alamat_pengiriman', 'nomor_telepon_pelanggan', 'kota', 'provinsi', 'kode_pos']
        widgets = {
            'nama_pelanggan': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_pengiriman': forms.Textarea(attrs={'class': 'form-control'}),
            'nomor_telepon_pelanggan': forms.TextInput(attrs={'class': 'form-control'}),
            'kota': forms.TextInput(attrs={'class': 'form-control'}),
            'provinsi': forms.TextInput(attrs={'class': 'form-control'}),
            'kode_pos': forms.TextInput(attrs={'class': 'form-control'}),
        }

