import re
                "balance-sheet"
            )

        else:

            df = get_moneycontrol_statement(url)

            st.warning(
                "Moneycontrol structure differs by company. "
                "You may need to customize mappings."
            )

            st.dataframe(df)
            st.stop()

        st.subheader("Income Statement")
        st.dataframe(income_statement)

        st.subheader("Balance Sheet")
        st.dataframe(balance_sheet)

        years = list(income_statement.columns)

        if len(years) < 2:
            st.error("At least 2 years of financial data required")
            st.stop()

        current_year = years[0]
        previous_year = years[1]

        st.write(f"Using Current Year: {current_year}")
        st.write(f"Using Previous Year: {previous_year}")

        metrics = calculate_beneish(
            balance_sheet,
            income_statement,
            current_year,
            previous_year
        )

        st.subheader("Beneish Variables")

        metrics_df = pd.DataFrame(
            metrics.items(),
            columns=["Metric", "Value"]
        )

        st.dataframe(metrics_df)

        m_score = metrics["M-Score"]

        st.header(f"Beneish M-Score: {round(m_score, 2)}")

        if m_score > -2.22:
            st.error(
                "Potential earnings manipulation risk detected."
            )
        else:
            st.success(
                "Company appears less likely to be manipulating earnings."
            )

    except Exception as e:
        st.exception(e)
