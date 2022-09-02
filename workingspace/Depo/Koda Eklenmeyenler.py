# ---#
        st.subheader("Total Activity Duration - (Request Types-Sınıf_Tipi)")
        piv = df1.pivot_table(index="İstek_Tipi_Detay", columns="Sınıf_Tipi", values="Toplam_Aktivite_Süresi")
        st.write(piv)
        st.subheader("Total Sla Duration - (Request Types-Sınıf_Tipi)")
        piv2 = df1.pivot_table(index="İstek_Tipi_Detay", columns="Sınıf_Tipi", values="Sla_Süresi")
        st.write(piv2)